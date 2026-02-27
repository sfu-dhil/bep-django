
export const _getPaginatedApiResources = async (request) => {
  let pagedRequest = request
  let results = []
  try {
    while(pagedRequest) {
      const response = await fetch(pagedRequest, {mode: 'cors'})
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      }
      const data = await response.json()
      results = results.concat(data.results)
      pagedRequest = data.next || null
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  }
  return results
}

export const _getApiResource = async (request) => {
  try {
    const response = await fetch(request, {mode: 'cors'})
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`)
    }
    return await response.json()
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

export const _generateBasicApiResourceStore = (resourcesApiUrl) => {
  return {
    state: () => ({
      loadedObjects: [],
    }),
    getters: {
      objectMap: (state) => state.loadedObjects.reduce((result, o) => result.set(o.id, o), new Map()),
    },
    actions: {
      async getById(id) {
        if (!id || !Number.isInteger(id) || id <= 0) { return null }
        if (this.objectMap.has(id)) { return this.objectMap.get(id) }

        this.loadedObjects = await _getPaginatedApiResources(resourcesApiUrl)
        return this.objectMap.get(id)
      },
      async getAll() {
        if (this.loadedObjects.length > 0) { return this.loadedObjects }

        this.loadedObjects = await _getPaginatedApiResources(resourcesApiUrl)
        return this.loadedObjects
      },
    },
    persist: {
      storage: sessionStorage
    },
  }
}


export const _generateParishDependantApiResourceStore = (resourceApiUrlFunction, parishResourcesApiUrlFunction) => {
  return {
    state: () => ({
      loadedObjects: [],
    }),
    getters: {
      objectMap: (state) => state.loadedObjects.reduce((result, o) => result.set(o.id, o), new Map()),
      parishObjectMap: (state) => state.loadedObjects.reduce((result, o) => {
        if (!result.has(o.parish_id)) { result.set(o.parish_id, []) }
        result.get(o.parish_id).push(o)
        return result
      }, new Map()),
    },
    actions: {
      async getById(id) {
        if (!id || !Number.isInteger(id) || id <= 0) { return null }
        if (this.objectMap.has(id)) { return this.objectMap.get(id) }

        const resource = await _getApiResource(resourceApiUrlFunction(id))
        this.loadedObjects.push(resource)
        return resource
      },
      async getByParishId(id) {
        if (!id || !Number.isInteger(id) || id <= 0) { return null }
        if (this.parishObjectMap.has(id)) { return this.parishObjectMap.get(id) }

        const resources = await _getPaginatedApiResources(parishResourcesApiUrlFunction(id))
        resources.filter((o) => !this.objectMap.has(o.id)).forEach((o) => this.loadedObjects.push(o))
        return resources
      },
    },
    persist: {
      storage: sessionStorage
    },
  }
}
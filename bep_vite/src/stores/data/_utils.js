
export const _getPaginatedApiResources = async (resourceName) => {
  let request = `/api/${resourceName}`
  let results = []
  try {
    while(request) {
      const response = await fetch(request, {mode: 'cors'})
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`)
      }
      const data = await response.json()
      results = results.concat(data.results)
      request = data.next || null
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  }
  return results
}

export const _generateBookMap = (dataset) => dataset.reduce((result, o) => {
  o.books.forEach(bookId => {
    if (!result.has(bookId)) {
      result.set(bookId, new Set())
    }
    result.get(bookId)?.add(o.id)
  })
  return result
}, new Map())

export const _generateParishMap = (dataset) => dataset.reduce((result, o) => {
  if (!result.has(o.parish_id)) {
    result.set(o.parish_id, new Set())
  }
  result.get(o.parish_id)?.add(o.id)
  return result
}, new Map())

export const _getItemsContainingBooks = (bookIds, itemMap, bookItemMap) => {
  const itemIds = bookIds.reduce((result, bookId) => {
    if (bookItemMap.has(bookId)) {
      result = result.union(bookItemMap.get(bookId))
    }
    return result
  }, new Set())
  return [...itemIds.values()].map((id) => itemMap.get(id))
}

export const _getParishItems = (parishId, itemMap, parishItemMap) => parishItemMap.has(parishId) ? [...parishItemMap.get(parishId).values()].map((id) => itemMap.get(id)) : []


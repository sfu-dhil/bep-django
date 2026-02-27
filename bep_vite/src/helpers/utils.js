

const _filterBySetIds = (objectParam, ids) => ids.size === 0 ? () => true : (o) => ids.has(o[objectParam])
const _filterById = (objectParam, id) => id === null ? () => true : (o) => id == o[objectParam]

export const filterByNationSetIds = (ids) => _filterBySetIds('nation_id', ids)
export const filterByNationId = (id) => _filterById('nation_id', id)

export const FilterByCountySetIds = (ids) => _filterBySetIds('county_id', ids)
export const filterByCountyId = (id) => _filterById('county_id', id)

export const filterByTownSetIds = (ids) => _filterBySetIds('town_id', ids)
export const filterByTownId = (id) => _filterById('town_id', id)

export const filterByProvinceSetIds = (ids) => _filterBySetIds('province_id', ids)
export const filterByProvinceId = (id) => _filterById('province_id', id)

export const filterByDioceseSetIds = (ids) => _filterBySetIds('diocese_id', ids)
export const filterByDioceseId = (id) => _filterById('diocese_id', id)

export const filterByArchdeaconrySetIds = (ids) => _filterBySetIds('archdeaconry_id', ids)
export const filterByArchdeaconryId = (id) => _filterById('archdeaconry_id', id)

export const filterByParishSetIds = (ids) => _filterBySetIds('parish_id', ids)
export const filterByParishId = (id) => _filterById('parish_id', id)

export const formattedDateRange = (dates) => {
  dates = dates.filter((d) => d !== null && d != '1000-01-01')
  if (dates.length === 0) { return null }

  const startDate = new Date(Math.min(...dates))
  const endDate = new Date(Math.max(...dates))
  if (startDate.getFullYear() != endDate.getFullYear()) {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric' })}-${endDate.toLocaleString('en-CA', { year: 'numeric' })}`
  } else if (startDate.getMonth() != endDate.getMonth()) {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric', month: 'long' })} to ${endDate.toLocaleString('en-CA', { year: 'numeric', month: 'long' })}`
  } else {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric', month: 'long' })}`
  }
}
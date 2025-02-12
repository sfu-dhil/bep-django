const _filterByIds = (objectParam, ids) => ids.length === 0 ? () => true : (o) => ids.includes(o[objectParam])
const _filterById = (objectParam, id) => id === null ? () => true : (o) => id == o[objectParam]

export const filterByNationIds = (ids) => _filterByIds('nation_id', ids)
export const filterByNationId = (id) => _filterById('nation_id', id)

export const FilterByCountyIds = (ids) => _filterByIds('county_id', ids)
export const filterByCountyId = (id) => _filterById('county_id', id)

export const filterByTownIds = (ids) => _filterByIds('town_id', ids)
export const filterByTownId = (id) => _filterById('town_id', id)

export const filterByProvinceIds = (ids) => _filterByIds('province_id', ids)
export const filterByProvinceId = (id) => _filterById('province_id', id)

export const filterByDioceseIds = (ids) => _filterByIds('diocese_id', ids)
export const filterByDioceseId = (id) => _filterById('diocese_id', id)

export const filterByArchdeaconryIds = (ids) => _filterByIds('archdeaconry_id', ids)
export const filterByArchdeaconryId = (id) => _filterById('archdeaconry_id', id)

export const filterByParishIds = (ids) => _filterByIds('parish_id', ids)
export const filterByParishId = (id) => _filterById('parish_id', id)

export const filterByBookIds = (ids) => {
  const bookIdsSet = new Set(ids)
  return ids.length === 0 ? () => true : (o) => bookIdsSet.intersection(new Set(o.books)).size > 0
}
export const filterByBookId = (id) => {
  return id != null ? () => true : (o) => o.books.includes(id)
}
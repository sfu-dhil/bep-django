

const _filterByObjectId = (objectParam, id) => id === null ? () => true : (o) => id == o[objectParam]?.id
export const filterByNationId = (id) => _filterByObjectId('nation', id)
export const filterByCountyId = (id) => _filterByObjectId('county', id)
export const filterByTownId = (id) => _filterByObjectId('town', id)
export const filterByProvinceId = (id) => _filterByObjectId('province', id)
export const filterByDioceseId = (id) => _filterByObjectId('diocese', id)
export const filterByArchdeaconryId = (id) => _filterByObjectId('archdeaconry', id)
export const filterByParishId = (id) => _filterByObjectId('parish', id)

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
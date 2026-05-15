

const _filterByObjectId = (objectParam, id) => id === null ? () => true : (o) => id == o[objectParam]?.id
export const filterByNationId = (id) => _filterByObjectId('nation', id)
export const filterByCountyId = (id) => _filterByObjectId('county', id)
export const filterByTownId = (id) => _filterByObjectId('town', id)
export const filterByProvinceId = (id) => _filterByObjectId('province', id)
export const filterByDioceseId = (id) => _filterByObjectId('diocese', id)
export const filterByArchdeaconryId = (id) => _filterByObjectId('archdeaconry', id)
export const filterByParishId = (id) => _filterByObjectId('parish', id)

export const formattedDateRange = (dates) => {
  dates = dates.filter((d) => d !== null)
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

export const formattedYearRange = (years) => {
  years = years.filter((d) => d !== null)
  if (years.length === 0) { return null }

  const startDate = new Date(Math.min(...years), 0)
  const endDate = new Date(Math.max(...years), 0)
  if (startDate.getFullYear() != endDate.getFullYear()) {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric' })}-${endDate.toLocaleString('en-CA', { year: 'numeric' })}`
  } else {
    return `${startDate.toLocaleString('en-CA', { year: 'numeric' })}`
  }
}


export const getLsd = (totalPence) => {
  if (!totalPence) { totalPence = 0 }
  return { l: Math.floor(Math.abs(totalPence)/240), s: Math.floor((Math.abs(totalPence) % 240) / 12), d: Math.floor((Math.abs(totalPence) % 240) % 12) }
}
export const getLsdString = (totalPence) => {
  const {l, s, d} = getLsd(totalPence)
  if (l === 0 && s === 0 && d === 0) { return '0d' }
  const lsdParts = []
  let lsdTotal = ''
  if (l > 0) { lsdParts.push(`£${l}`) }
  if (s > 0) { lsdParts.push(`${s}s`) }
  if (d > 0) { lsdParts.push(`${d}d`) }
  if (l > 0 || s > 0) { lsdTotal = `(${totalPence}d)` }
  return `${lsdParts.join('. ')} ${lsdTotal}`
}

const CUSTOM_COLOR_PALLETTE = ['#003f5c', '#2f4b7c', '#665191', '#a05195', '#d45087', '#f95d6a', '#ff7c43', '#ffa600']
export const getColorPalletByIndex = (index) => CUSTOM_COLOR_PALLETTE[index % CUSTOM_COLOR_PALLETTE.length]
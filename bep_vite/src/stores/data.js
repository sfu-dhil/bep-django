const nationMap = JSON.parse(document.getElementById('bep-nations-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const countyMap = JSON.parse(document.getElementById('bep-counties-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const townMap = JSON.parse(document.getElementById('bep-towns-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const provinceMap = JSON.parse(document.getElementById('bep-provinces-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const dioceseMap = JSON.parse(document.getElementById('bep-dioceses-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const archdeaconryMap = JSON.parse(document.getElementById('bep-archdeaconries-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const parishMap = JSON.parse(document.getElementById('bep-parishes-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const monarchMap = JSON.parse(document.getElementById('bep-monarchs-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())

const bookMap = JSON.parse(document.getElementById('bep-books-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const transactionMap = JSON.parse(document.getElementById('bep-transactions-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const inventoryMap = JSON.parse(document.getElementById('bep-inventories-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())
const holdingMap = JSON.parse(document.getElementById('bep-holdings-data').textContent)
  .reduce((result, o) => result.set(o.id, o), new Map())

const _generateBookMap = (dataset) => dataset.reduce((result, o) => {
  o.books.forEach(bookId => {
    if (!result.has(bookId)) {
      result.set(bookId, new Set())
    }
    result.get(bookId)?.add(o.id)
  })
  return result
}, new Map())
const bookTransactionMap = _generateBookMap([...transactionMap.values()])
const bookInventoryMap = _generateBookMap([...inventoryMap.values()])
const bookHoldingMap = _generateBookMap([...holdingMap.values()])

const _generateParishMap = (dataset) => dataset.reduce((result, o) => {
  if (!result.has(o.parish_id)) {
    result.set(o.parish_id, new Set())
  }
  result.get(o.parish_id)?.add(o.id)
  return result
}, new Map())
const parishTransactionMap = _generateParishMap([...transactionMap.values()])
const parishInventoryMap = _generateParishMap([...inventoryMap.values()])
const parishHoldingMap = _generateParishMap([...holdingMap.values()])

const _getItemsContainingBooks = (bookIds, itemMap, bookItemMap) => {
  const itemIds = bookIds.reduce((result, bookId) => {
    if (bookItemMap.has(bookId)) {
      result = result.union(bookItemMap.get(bookId))
    }
    return result
  }, new Set())
  return [...itemIds.values()].map((id) => itemMap.get(id))
}
const getTransactionsContainingBooks = (bookIds) => _getItemsContainingBooks(bookIds, transactionMap, bookTransactionMap)
const getInventoriesContainingBooks = (bookIds) => _getItemsContainingBooks(bookIds, inventoryMap, bookInventoryMap)
const getHoldingsContainingBooks = (bookIds) => _getItemsContainingBooks(bookIds, holdingMap, bookHoldingMap)

const _getParishItems = (parishId, itemMap, parishItemMap) => parishItemMap.has(parishId) ? [...parishItemMap.get(parishId).values()].map((id) => itemMap.get(id)) : []
const getParishTransactions = (parishId) => _getParishItems(parishId, transactionMap, parishTransactionMap)
const getParishInventories = (parishId) => _getParishItems(parishId, inventoryMap, parishInventoryMap)
const getParishHoldings = (parishId) => _getParishItems(parishId, holdingMap, parishHoldingMap)

export const useData = () => {
  return {
    nationMap,
    countyMap,
    townMap,
    provinceMap,
    dioceseMap,
    archdeaconryMap,
    parishMap,
    monarchMap,

    bookMap,
    transactionMap,
    inventoryMap,
    holdingMap,

    getTransactionsContainingBooks,
    getInventoriesContainingBooks,
    getHoldingsContainingBooks,
    getParishTransactions,
    getParishInventories,
    getParishHoldings,
  }
}
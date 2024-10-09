export const isSameObjectArray = (a, aParam, b, bParam) => {
    const aSet = new Set(a.map((o) => o[aParam]))
    const bSet = new Set(b.map((o) => o[bParam]))
    return aSet.symmetricDifference(bSet).size === 0
}

export const isSameObjectArrayById = (a, b) => {
    return isSameObjectArray(a, 'id', b, 'id')
}

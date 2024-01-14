const BASE_URL = "http://127.0.0.1:8000/api/v1/"

export const fetchLastProducts = async () => {
  return await fetch(`${BASE_URL}stock/`).then(r => r.json())
}

export const fetchItem = async id => {
  return await fetch(`${BASE_URL}items/${id}/`).then(r => r.json())
}

export const fetchProduct = async id => {
  return await fetch(`${BASE_URL}stock/${id}/`).then(r => r.json())
}

export const fetchProducts = async id => {
  return await fetch(`${BASE_URL}stock/?kind=${id}`).then(r =>
    r.status === 400 ? [] : r.json()
  )
}

export const fetchCategory = async slug => {
  return await fetch(`${BASE_URL}categories/?slug=${slug}`)
    .then(r => r.json())
    .then(r => r.at(0))
}

export const fetchRootCategories = async () => {
  return await fetch(`${BASE_URL}categories/?root=true`).then(r => r.json())
}

export const fetchChildCategories = async id => {
  return await fetch(`${BASE_URL}categories/?parent=${id}`).then(r =>
    r.status === 400 ? [] : r.json()
  )
}
const BASE_URL = "http://127.0.0.1:8000/api/v1/"

class ArcHttpClient {
  #options = {
    headers: { "Content-type": "application/json; charset=UTF-8" },
  }

  #cb = r => r.json()

  constructor(base_url) {
    this.root = base_url
  }

  async get(path, cb = this.#cb) {
    return await fetch(this.root + path).then(cb)
  }

  async post(path, cb = this.#cb) {
    return await fetch(this.root + path, {
      method: "POST",
      body: JSON.stringify(data),
      ...this.#options,
    }).then(cb)
  }

  async patch(path, data, cb = this.#cb) {
    return await fetch(this.root + path, {
      method: "PATCH",
      body: JSON.stringify(data),
      ...this.#options,
    }).then(cb)
  }

  async delete(path, cb = this.#cb) {
    return await fetch(this.root + path, {
      method: "DELETE",
    }).then(cb)
  }
}

const client = new ArcHttpClient(BASE_URL)

export const fetchItem = async id => await client.get(`items/${id}/`)

export const patchItem = async (id, data) => await client.patch(`items/${id}/`, data)

export const deleteItem = async id => await client.delete(`items/${id}/`)

export const fetchProducts = async (kindId = null) =>
  kindId !== null
    ? await client.get(`stock/?kind=${kindId}`, r => (r.status !== 400 ? r.json() : []))
    : await client.get(`stock/`)

export const fetchLastProducts = async () => await client.get("stock/")

export const fetchProduct = async id => await client.get(`stock/${id}/`)

export const fetchCategory = async slug =>
  await client.get(`categories/?slug=${slug}`).then(r => r.at(0))

export const fetchRootCategories = async () => await client.get(`categories/?root=true`)

export const fetchChildCategories = async id =>
  await client.get(`categories/?parent=${id}`, r => (r.status !== 400 ? r.json() : []))

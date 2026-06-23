import { useEffect, useState } from "react";
import api from "../../api";
import { useParams, useNavigate } from "react-router-dom";

export default function ProductForm() {
  const { id } = useParams();
  const navigate = useNavigate();

  const isEdit = Boolean(id);

  const [data, setData] = useState({
    name: "",
    price: "",
    stock: "",
    category_id: "",
    image_url: ""
  });

  // LOAD PRODUCT FOR EDIT
  useEffect(() => {
    if (isEdit) {
      api.get(`/api/products/${id}`).then(res => {
        const p = res.data;

        setData({
          name: p.name || "",
          price: p.price || "",
          stock: p.stock || "",
          category_id: p.category_id || "",
          image_url: p.image_url || ""
        });
      });
    }
  }, [id]);

  // HANDLE INPUT CHANGE
  const handleChange = (e) => {
    setData({ ...data, [e.target.name]: e.target.value });
  };

  // SUBMIT
  const submit = async () => {
    try {
      if (isEdit) {
        await api.put(`/api/products/${id}`, data);
      } else {
        await api.post("/api/products", data);
      }

      navigate("/admin/products");
    } catch (err) {
      console.log(err);
      alert("Error saving product");
    }
  };

  return (
    <div className="container" style={{ maxWidth: "500px" }}>
      <h2>{isEdit ? "Edit Product" : "Add Product"}</h2>

      <input
        name="name"
        placeholder="Name"
        value={data.name}
        onChange={handleChange}
      />

      <input
        name="price"
        placeholder="Price"
        value={data.price}
        onChange={handleChange}
      />

      <input
        name="stock"
        placeholder="Stock"
        value={data.stock}
        onChange={handleChange}
      />

      <input
        name="category_id"
        placeholder="Category ID"
        value={data.category_id}
        onChange={handleChange}
      />

      <input
        name="image_url"
        placeholder="Image URL"
        value={data.image_url}
        onChange={handleChange}
      />

      <button onClick={submit}>
        {isEdit ? "Update Product" : "Add Product"}
      </button>
    </div>
  );
}
import { useEffect, useState } from "react";
import api from "../api";
import { useCart } from "../context/CartContext";
import { useLocation } from "react-router-dom";
import { getImage } from "../utils/image"; // ✅ IMPORTANT

export default function Home() {
  const [products, setProducts] = useState([]);
  const [category, setCategory] = useState("");

  const { addToCart } = useCart();
  const location = useLocation();

  const queryParams = new URLSearchParams(location.search);
  const search = queryParams.get("search") || "";

  // Load products
  useEffect(() => {
    api.get("/api/products")
      .then((res) => setProducts(res.data || []))
      .catch((err) => console.log(err));
  }, []);

  // Filter logic
  const filteredProducts = products.filter((p) => {
    const matchName =
      p.name?.toLowerCase().includes(search.toLowerCase());

    const matchCategory =
      category === "" ||
      p.category?.toLowerCase() === category.toLowerCase();

    return matchName && matchCategory;
  });

  return (
    <div className="container">

      <h2 className="page-title">🛍️ Products</h2>

      {/* Category Filter */}
      <div className="search-bar">
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="">All Categories</option>
          <option value="Electronics">Electronics</option>
          <option value="Groceries">Groceries</option>
          <option value="Toys">Toys</option>
          <option value="Beauty">Beauty</option>
          <option value="Fashion">Fashion</option>
          <option value="Books">Books</option>
          <option value="Home & Kitchen">Home & Kitchen</option>
          <option value="Sports">Sports</option>
        </select>
      </div>

      {/* Search text */}
      {search && (
        <p style={{ marginBottom: "10px" }}>
          🔍 Search result for: <b>{search}</b>
        </p>
      )}

      {/* Products */}
      <div className="product-grid">

        {filteredProducts.length > 0 ? (
          filteredProducts.map((product) => (
            <div className="product-card" key={product.id}>

              {/* ✅ FIXED IMAGE */}
              <img
                src={getImage(product.image_url)}
                alt={product.name}
                loading="lazy"
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src =
                    "https://placehold.co/300x300?text=No+Image";
                }}
              />

              <h3>{product.name}</h3>
              <p>₹ {product.price}</p>
              <p>{product.category}</p>

              <button
                className="btn"
                onClick={() => {
                  addToCart(product, 1);
                  alert("Added to cart 🛒");
                }}
              >
                Add to Cart
              </button>

            </div>
          ))
        ) : (
          <p>No products found 😢</p>
        )}

      </div>

    </div>
  );
}
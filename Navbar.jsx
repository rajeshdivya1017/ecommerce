import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useCart } from "../context/CartContext";
import { useAuth } from "../context/AuthContext";
import api from "../api";

export default function Navbar() {
  const { cartItems = [] } = useCart();
  const { user, setUser } = useAuth();
  const navigate = useNavigate();

  const [search, setSearch] = useState("");

  const totalItems = cartItems.reduce(
    (sum, item) => sum + (item.qty || 1),
    0
  );

  const logout = async () => {
    try {
      await api.get("/api/logout");
    } catch (err) {}

    setUser(null);
    localStorage.removeItem("token");
    navigate("/login");
  };

  const handleSearch = () => {
    // 👉 search query URL-க்கு send பண்ணுறோம்
    navigate(`/?search=${search}`);
  };

  return (
    <div className="navbar">

      <h2>🛒 E-Commerce</h2>

      {/* SEARCH BOX */}
      <div className="search-box">
        <input
          type="text"
          placeholder="Search products..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <button className="search-btn" onClick={handleSearch}>
          Search
        </button>
      </div>

      <div className="nav-links">

        <Link to="/">Home</Link>

        {user?.role !== "admin" && (
          <>
            <Link to="/cart">Cart ({totalItems})</Link>
            <Link to="/orders">My Orders</Link>
          </>
        )}

        {user?.role === "admin" && (
          <>
            <Link to="/admin/products">Products</Link>
            <Link to="/admin/orders">Orders</Link>
          </>
        )}

        {!user ? (
          <Link to="/login">Login</Link>
        ) : (
          <>
            <span>👤 {user.name}</span>

            <button className="logout-btn" onClick={logout}>
              Logout
            </button>
          </>
        )}

      </div>

    </div>
  );
}
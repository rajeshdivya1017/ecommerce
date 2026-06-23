import { useCart } from "../context/CartContext";
import api from "../api";
import { useState } from "react";

export default function Cart() {
  const { cartItems = [], removeFromCart, clearCart } = useCart();
  const [address, setAddress] = useState("");

  const total = cartItems.reduce(
    (sum, i) => sum + i.price * i.qty,
    0
  );

  const placeOrder = async () => {
    try {
      const res = await api.post("/api/orders", {
        address,
        items: cartItems.map((i) => ({
          product_id: i.id,
          quantity: i.qty,
        })),
      });

      alert(res.data.message);
      clearCart();
    } catch (err) {
      alert(err.response?.data?.message || "Order failed");
    }
  };

  return (
    <div className="container">
      <h2>🛒 Cart</h2>

      {cartItems.map((i) => (
        <div className="cart-item" key={i.id}>
          <h3>{i.name}</h3>
          <p>Qty: {i.qty}</p>
          <p>₹ {i.price * i.qty}</p>

          <button onClick={() => removeFromCart(i.id)}>
            Remove
          </button>
        </div>
      ))}

      <h3>Total: ₹ {total}</h3>

      <input
        placeholder="Delivery Address"
        value={address}
        onChange={(e) => setAddress(e.target.value)}
      />

      <button onClick={placeOrder}>
        Place Order
      </button>
    </div>
  );
}
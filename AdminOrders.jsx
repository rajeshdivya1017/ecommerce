import { useEffect, useState } from "react";
import api from "../../api";

export default function AdminOrders() {
  const [orders, setOrders] = useState([]);

  const load = () => {
    api.get("/api/admin/orders")
      .then(res => setOrders(res.data));
  };

  useEffect(() => {
    load();
  }, []);

  const updateStatus = async (id, status) => {
    await api.put(`/api/orders/${id}/status`, { status });
    load();
  };

  return (
    <div className="container">
      <h2>Admin Orders</h2>

      {orders.map(o => (
        <div className="card" key={o.id}>
          <h3>Order #{o.id}</h3>
          <p>{o.customer_name}</p>
          <p>Total: ₹{o.total_amount}</p>

          <select
            value={o.status}
            onChange={(e) => updateStatus(o.id, e.target.value)}
          >
            <option>Pending</option>
            <option>Confirmed</option>
            <option>Shipped</option>
            <option>Delivered</option>
            <option>Cancelled</option>
          </select>
        </div>
      ))}
    </div>
  );
}
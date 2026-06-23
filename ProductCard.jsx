import { Link } from "react-router-dom";
import { useCart } from "../context/CartContext";
import { getImage } from "../utils/image";

export default function ProductCard({ product }) {
  const { addToCart } = useCart();

  return (
    <div className="card">

      {/* IMAGE FIX */}
      <img
        src={getImage(product.image_url)}
        alt={product.name}
      />

      <h3>{product.name}</h3>
      <p>₹ {product.price}</p>
      <p>{product.category}</p>

      <Link to={`/product/${product.id}`}>
        <button>View</button>
      </Link>

      <button onClick={() => addToCart(product, 1)}>
        Add to Cart
      </button>
    </div>
  );
}
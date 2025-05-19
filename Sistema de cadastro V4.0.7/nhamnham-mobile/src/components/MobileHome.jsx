import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { motion } from 'framer-motion';
import Cadastro from './Cadastro';
import '../style.css';

import sushiImg from './img/sushi.png';
import labonatti from './img/pizzaria-labonatti.jpg';
import hamburguer from './img/casa-do-hamburguer.png';

const sampleRestaurants = [
  { id: 1, name: 'Pizzaria La Bonatti', cuisine: 'Pizza', image: labonatti, rating: 4.5, deliveryTime: '30-40 min' },
  { id: 2, name: 'Casa do Hamburguer', cuisine: 'Burger', image: hamburguer, rating: 4.2, deliveryTime: '20-30 min' },
  { id: 3, name: 'Sushi Express', cuisine: 'Sushi', image: sushiImg, rating: 4.8, deliveryTime: '25-35 min' },
];

export default function MobileHome() {
  const [searchTerm, setSearchTerm] = useState('');
  const [restaurants, setRestaurants] = useState(sampleRestaurants);
  const [showCadastro, setShowCadastro] = useState(false);

  useEffect(() => {
    setRestaurants(
      sampleRestaurants.filter(r =>
        r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        r.cuisine.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [searchTerm]);

  if (showCadastro) {
    return <Cadastro onBack={() => setShowCadastro(false)} />;
  }

  return (
    <div className="container">
      <header className="header">
        <h1 className="logo">NhamNham</h1>
        <div className="search-wrapper">
          <Search className="search-icon" />
          <input
            type="text"
            placeholder="Buscar restaurantes"
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>
      </header>

      <main className="restaurant-list">
        {restaurants.length ? (
          restaurants.map(restaurant => (
            <motion.div
              key={restaurant.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className="restaurant-card"
            >
              <img
                src={restaurant.image}
                alt={restaurant.name}
                className="restaurant-img"
              />
              <div className="restaurant-info">
                <h2 className="restaurant-name">{restaurant.name}</h2>
                <p className="restaurant-cuisine">{restaurant.cuisine}</p>
                <div className="restaurant-meta">
                  <span className="rating">⭐ {restaurant.rating}</span>
                  <span className="delivery-time">{restaurant.deliveryTime}</span>
                </div>
              </div>
            </motion.div>
          ))
        ) : (
          <p className="no-results">Nenhum restaurante encontrado.</p>
        )}
      </main>

      <nav className="bottom-nav">
        <button className="nav-button active" onClick={() => setShowCadastro(false)}>
          Home
        </button>
        <button className="nav-button">Pedidos</button>
        <button className="nav-button" onClick={() => setShowCadastro(true)}>
          Cadastro
        </button>
        <button className="nav-button">Perfil</button>
      </nav>
    </div>
  );
}
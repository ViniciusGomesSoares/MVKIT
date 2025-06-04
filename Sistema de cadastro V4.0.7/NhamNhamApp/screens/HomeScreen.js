import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, FlatList, Image, TouchableOpacity, StyleSheet } from 'react-native';

const sampleRestaurants = [
  { id: '1', name: 'Pizzaria La Bonatti', cuisine: 'Pizza', image: require('../assets/pizzaria-labonatti.jpg'), rating: 4.5, deliveryTime: '30-40 min' },
  { id: '2', name: 'Casa do Hamburguer', cuisine: 'Burger', image: require('../assets/casa-do-hamburguer.png'), rating: 4.2, deliveryTime: '20-30 min' },
  { id: '3', name: 'Sushi Express', cuisine: 'Sushi', image: require('../assets/sushi.png'), rating: 4.8, deliveryTime: '25-35 min' },
];

export default function HomeScreen({ navigation }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [restaurants, setRestaurants] = useState(sampleRestaurants);

  useEffect(() => {
    const filtered = sampleRestaurants.filter(r =>
      r.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.cuisine.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setRestaurants(filtered);
  }, [searchTerm]);

  const renderRestaurant = ({ item }) => (
    <View style={styles.card}>
      <Image source={item.image} style={styles.image} />
      <View style={styles.info}>
        <Text style={styles.name}>{item.name}</Text>
        <Text style={styles.cuisine}>{item.cuisine}</Text>
        <View style={styles.meta}>
          <Text style={styles.rating}>⭐ {item.rating}</Text>
          <Text style={styles.delivery}>{item.deliveryTime}</Text>
        </View>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>NhamNham</Text>
      <TextInput
        style={styles.searchInput}
        placeholder="Buscar restaurantes"
        value={searchTerm}
        onChangeText={setSearchTerm}
      />

      {restaurants.length ? (
        <FlatList
          data={restaurants}
          keyExtractor={(item) => item.id}
          renderItem={renderRestaurant}
        />
      ) : (
        <Text style={styles.noResults}>Nenhum restaurante encontrado.</Text>
      )}

      <TouchableOpacity
        style={styles.cadastroButton}
        onPress={() => navigation.navigate('Cadastro')}
      >
        <Text style={styles.cadastroButtonText}>Ir para Cadastro</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20, backgroundColor: '#fff' },
  logo: { fontSize: 32, fontWeight: 'bold', marginBottom: 20, alignSelf: 'center' },
  searchInput: {
    borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 10, marginBottom: 20,
  },
  card: {
    flexDirection: 'row', marginBottom: 15, backgroundColor: '#f5f5f5', borderRadius: 10, overflow: 'hidden',
  },
  image: { width: 80, height: 80 },
  info: { flex: 1, padding: 10 },
  name: { fontWeight: 'bold', fontSize: 18 },
  cuisine: { color: '#666', marginTop: 4 },
  meta: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 10 },
  rating: { color: '#f1c40f', fontWeight: 'bold' },
  delivery: { color: '#888' },
  noResults: { textAlign: 'center', marginTop: 50, fontSize: 18, color: '#888' },
  cadastroButton: {
    marginTop: 20, backgroundColor: '#4caf50', padding: 15, borderRadius: 8, alignItems: 'center',
  },
  cadastroButtonText: { color: '#fff', fontWeight: 'bold', fontSize: 16 },
});

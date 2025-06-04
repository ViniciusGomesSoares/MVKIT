import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, Alert, StyleSheet, ScrollView } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function CadastroScreen() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');
  const [codigoGerado, setCodigoGerado] = useState('');
  const [codigoDigitado, setCodigoDigitado] = useState('');
  const [valido, setValido] = useState(false);
  const [pessoas, setPessoas] = useState([]);

  useEffect(() => {
    const carregarDados = async () => {
      try {
        const jsonValue = await AsyncStorage.getItem('@CadastroReact');
        if (jsonValue != null) {
          setPessoas(JSON.parse(jsonValue));
        }
      } catch (e) {
        console.error('Erro ao carregar dados', e);
      }
    };

    carregarDados();
  }, []);

  useEffect(() => {
    const salvarDados = async () => {
      try {
        const jsonValue = JSON.stringify(pessoas);
        await AsyncStorage.setItem('@CadastroReact', jsonValue);
      } catch (e) {
        console.error('Erro ao salvar dados', e);
      }
    };

    salvarDados();
  }, [pessoas]);

  const gerarCodigo = () => {
    return Math.floor(100000 + Math.random() * 900000).toString();
  };

  const handleCadastro = () => {
    if (!nome || !email || !telefone) {
      Alert.alert('Preencha todos os campos!');
      return;
    }

    const novoCodigo = gerarCodigo();
    setCodigoGerado(novoCodigo);
    setValido(false);

    const novaPessoa = {
      nome,
      email,
      telefone,
      codigo: novoCodigo,
    };

    setPessoas([...pessoas, novaPessoa]);
    setNome('');
    setEmail('');
    setTelefone('');

    Alert.alert('Cadastro realizado!', `Código de autenticação: ${novoCodigo}`);
  };

  const handleValidarCodigo = () => {
    const encontrado = pessoas.find(p => p.codigo === codigoDigitado);
    if (encontrado) {
      setValido(true);
      Alert.alert('✅ Código validado com sucesso!');
    } else {
      setValido(false);
      Alert.alert('❌ Código inválido.');
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Cadastro de Usuário</Text>

      <TextInput
        style={styles.input}
        placeholder="Nome"
        value={nome}
        onChangeText={setNome}
      />
      <TextInput
        style={styles.input}
        placeholder="E-mail"
        keyboardType="email-address"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        style={styles.input}
        placeholder="Telefone"
        keyboardType="phone-pad"
        value={telefone}
        onChangeText={setTelefone}
      />

      <Button title="Cadastrar" onPress={handleCadastro} />

      {codigoGerado ? (
        <View style={styles.codigoBox}>
          <Text><Text style={{ fontWeight: 'bold' }}>Código gerado:</Text> {codigoGerado}</Text>
        </View>
      ) : null}

      <View style={styles.validarBox}>
        <Text style={styles.subtitle}>Validar Código</Text>
        <TextInput
          style={styles.input}
          placeholder="Digite o código recebido"
          value={codigoDigitado}
          onChangeText={setCodigoDigitado}
        />
        <Button title="Validar Código" onPress={handleValidarCodigo} />
        {valido && <Text style={styles.validMsg}>🎉 Código validado com sucesso!</Text>}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { padding: 20, backgroundColor: '#f5f5f5', flexGrow: 1 },
  title: { fontSize: 24, fontWeight: 'bold', marginBottom: 20, alignSelf: 'center' },
  input: {
    backgroundColor: '#fff', padding: 10, marginBottom: 15, borderRadius: 8, borderWidth: 1, borderColor: '#ccc',
  },
  codigoBox: {
    marginVertical: 20, padding: 15, backgroundColor: '#e3f2fd', borderRadius: 8,
  },
  validarBox: {
    marginTop: 10, padding: 15, backgroundColor: '#e3f2fd', borderRadius: 8,
  },
  subtitle: { fontWeight: 'bold', fontSize: 18, marginBottom: 10 },
  validMsg: { color: 'green', marginTop: 10, fontWeight: 'bold' },
});

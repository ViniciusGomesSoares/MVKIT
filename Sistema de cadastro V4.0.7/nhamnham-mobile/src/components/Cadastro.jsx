import React, { useState, useEffect } from 'react';
import './Cadastro.css';

function Cadastro() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');
  const [codigoGerado, setCodigoGerado] = useState('');
  const [codigoDigitado, setCodigoDigitado] = useState('');
  const [valido, setValido] = useState(false);
  const [pessoas, setPessoas] = useState([]);

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem('CadastroReact')) || [];
    setPessoas(saved);
  }, []);

  useEffect(() => {
    localStorage.setItem('CadastroReact', JSON.stringify(pessoas));
  }, [pessoas]);

  const gerarCodigo = () => {
    return Math.floor(100000 + Math.random() * 900000).toString(); // 6 dígitos
  };

  const handleCadastro = (e) => {
    e.preventDefault();
    const novoCodigo = gerarCodigo();
    setCodigoGerado(novoCodigo);
    setValido(false); // resetar validação anterior

    const novaPessoa = {
      nome,
      email,
      telefone,
      codigo: novoCodigo,
    };

    setPessoas([...pessoas, novaPessoa]);

    // Resetar campos
    setNome('');
    setEmail('');
    setTelefone('');

    alert(`Código de autenticação enviado: ${novoCodigo}`);
  };

  const handleValidarCodigo = () => {
    const encontrado = pessoas.find(p => p.codigo === codigoDigitado);
    if (encontrado) {
      setValido(true);
      alert('✅ Código validado com sucesso!');
    } else {
      setValido(false);
      alert('❌ Código inválido.');
    }
  };

  return (
    <div className="cadastro-container">
      <h2>Cadastro de Usuário</h2>
      <form onSubmit={handleCadastro}>
        <input
          type="text"
          placeholder="Nome"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="tel"
          placeholder="Telefone"
          value={telefone}
          onChange={(e) => setTelefone(e.target.value)}
          required
        />
        <button type="submit">Cadastrar</button>
      </form>

      {codigoGerado && (
        <div className="codigo-box">
          <strong>Código gerado:</strong> {codigoGerado}
        </div>
      )}

      <div className="validar-box">
        <h3>Validar Código</h3>
        <input
          type="text"
          placeholder="Digite o código recebido"
          value={codigoDigitado}
          onChange={(e) => setCodigoDigitado(e.target.value)}
        />
        <button onClick={handleValidarCodigo}>Validar Código</button>
        {valido && <p className="valido-msg">🎉 Código validado com sucesso!</p>}
      </div>
    </div>
  );
}

export default Cadastro;

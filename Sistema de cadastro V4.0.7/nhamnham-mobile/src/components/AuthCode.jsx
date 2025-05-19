import React, { useState, useEffect } from 'react';
import './AuthCode.css';

const AuthCode = () => {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [inputCode, setInputCode] = useState('');
  const [authSuccess, setAuthSuccess] = useState(false);

  // Gerar código randômico
  const generateCode = () => {
    return Math.floor(100000 + Math.random() * 900000).toString(); // 6 dígitos
  };

  // Envio do código
  const sendCode = () => {
    const generated = generateCode();
    localStorage.setItem('verifCode', generated);
    console.log(`🔐 Código gerado: ${generated}`); // Substituir por envio real
    setCode(generated);
    setStep(2);
  };

  // Verificação código
  const verifyCode = () => {
    const savedCode = localStorage.getItem('verifCode');
    if (inputCode === savedCode) {
      setAuthSuccess(true);
      localStorage.removeItem('verifCode');
    } else {
      alert('Código inválido. Tente novamente.');
    }
  };

  return (
    <div className="auth-container">
      {step === 1 && (
        <div>
          <h2>🔐 Entrar com E-mail</h2>
          <input
            type="email"
            placeholder="Digite seu e-mail"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <button onClick={sendCode}>Enviar Código</button>
        </div>
      )}

      {step === 2 && (
        <div>
          <h2>📩 Digite o Código</h2>
          <input
            type="text"
            placeholder="123456"
            value={inputCode}
            onChange={(e) => setInputCode(e.target.value)}
          />
          <button onClick={verifyCode}>Verificar</button>
          <p><small>(Ver código no console para testes)</small></p>
        </div>
      )}

      {authSuccess && (
        <div>
          <h2>✅ Autenticado com sucesso!</h2>
          <p>Bem-vindo, {email}</p>
        </div>
      )}
    </div>
  );
};

export default AuthCode;

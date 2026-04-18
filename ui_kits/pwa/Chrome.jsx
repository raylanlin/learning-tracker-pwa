// Modal.jsx — centered modal w/ spring entry
const Modal = ({ open, title, placeholder, onCancel, onConfirm }) => {
  const [value, setValue] = React.useState('');
  React.useEffect(() => { if (open) setValue(''); }, [open]);
  return (
    <div className={`modal-overlay ${open ? 'show' : ''}`} onClick={(e) => { if (e.target === e.currentTarget) onCancel(); }}>
      <div className="modal">
        <h2>{title}</h2>
        <input
          autoFocus
          placeholder={placeholder}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter' && value.trim()) onConfirm(value.trim()); }}
        />
        <div className="modal-btns">
          <button className="btn-cancel" onClick={onCancel}>取消</button>
          <button className="btn-confirm" onClick={() => value.trim() && onConfirm(value.trim())}>确认</button>
        </div>
      </div>
    </div>
  );
};

// AuthScreen.jsx — login gate
const AuthScreen = ({ onLogin }) => {
  const [u, setU] = React.useState('');
  const [p, setP] = React.useState('');
  const [err, setErr] = React.useState('');
  const submit = () => {
    if (!u || !p) { setErr('请输入账号和密码'); return; }
    if (u.toLowerCase() !== 'raylan' && u.toLowerCase() !== 'scarlett') { setErr('账号不存在'); return; }
    setErr('');
    onLogin(u);
  };
  return (
    <div className="auth-screen">
      <div className="auth-card">
        <h1>学习追踪</h1>
        <p>输入账号密码登录</p>
        <div style={{ color: 'var(--red)', fontSize: 13, marginBottom: 12, minHeight: 20 }}>{err}</div>
        <input placeholder="账号" value={u} onChange={(e) => setU(e.target.value)} />
        <input type="password" placeholder="密码" value={p} onChange={(e) => setP(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') submit(); }} />
        <button className="auth-btn" onClick={submit}>登录</button>
        <div className="auth-hint">数据将安全保存在云端 ☁️</div>
      </div>
    </div>
  );
};

// Fab.jsx — floating context-aware action
const Fab = ({ label, onClick }) => (
  <div className="fab-group">
    <button className="fab" onClick={onClick}>
      <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
        <path d="M9 3v12M3 9h12" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" />
      </svg>
      {label}
    </button>
  </div>
);

window.Modal = Modal;
window.AuthScreen = AuthScreen;
window.Fab = Fab;

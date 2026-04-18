// Header.jsx — app header with date + sync status pill
const Header = ({ dateLabel = '4月18日 周五', syncState = 'online' }) => {
  const statusText = {
    online: '● 在线',
    syncing: '⏳ 同步中…',
    synced: '● 已同步',
    error: '⚠ 同步失败',
    offline: '○ 离线',
  }[syncState] || '● 在线';
  return (
    <>
      <header className="app-header">
        <h1>学习追踪</h1>
        <span className="header-date">{dateLabel}</span>
      </header>
      <div className={`sync-status ${syncState}`}>{statusText}</div>
    </>
  );
};

window.Header = Header;

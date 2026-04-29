// TabBar.jsx — segmented tab switcher
const TabBar = ({ active, onChange }) => (
  <div className="tab-bar">
    <button className={`tab-btn ${active === 'calendar' ? 'active' : ''}`} onClick={() => onChange('calendar')}>📅 日历</button>
    <button className={`tab-btn ${active === 'grid' ? 'active' : ''}`} onClick={() => onChange('grid')}>🔲 网格</button>
  </div>
);

window.TabBar = TabBar;

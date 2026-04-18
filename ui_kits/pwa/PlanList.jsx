// PlanList.jsx — day detail with checkable plan items
const WEEKDAY_LONG = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
const formatDateCN = (dateStr) => {
  const d = new Date(dateStr + 'T00:00:00');
  return `${d.getMonth() + 1}月${d.getDate()}日 ${WEEKDAY_LONG[d.getDay()]}`;
};

const PlanList = ({ date, items = [], onToggle, onDelete, onAdd }) => (
  <div className="day-detail">
    <div className="day-detail-header">{formatDateCN(date)} · 计划</div>
    {items.length === 0 ? (
      <div style={{ padding: '16px', textAlign: 'center', color: 'var(--text-secondary)', fontSize: 14 }}>
        今天还没有计划
      </div>
    ) : items.map((it, i) => (
      <div key={it.id || i} className="calendar-task-item">
        <label className="calendar-task-checkbox">
          <input type="checkbox" checked={!!it.done} onChange={() => onToggle(i)} />
          <span className={`calendar-task-name ${it.done ? 'done' : ''}`}>{it.name}</span>
        </label>
        <button className="calendar-task-delete" onClick={() => onDelete(i)}>×</button>
      </div>
    ))}
    <button className="add-session-btn" onClick={onAdd}>+ 添加计划</button>
  </div>
);

window.PlanList = PlanList;
window.formatDateCN = formatDateCN;

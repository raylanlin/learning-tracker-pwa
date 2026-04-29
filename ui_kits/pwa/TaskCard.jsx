// TaskCard.jsx — collapsible task w/ subtasks + 60-cell grid
const TARGET = 30;

const Legend = () => (
  <div className="legend">
    <div className="legend-item"><div className="legend-dot" style={{ background: 'var(--gray)' }}></div>未完成</div>
    <div className="legend-item"><div className="legend-dot" style={{ background: 'var(--green)' }}></div>已完成</div>
    <div className="legend-item"><div className="legend-dot" style={{ background: 'var(--yellow)', boxShadow: '0 0 0 2px rgba(255,204,0,0.3)' }}></div>今日</div>
    <div className="legend-item"><div className="legend-dot" style={{ background: 'var(--purple)' }}></div>超额（&gt;30）</div>
  </div>
);

const CellGrid = ({ cells, onCellClick }) => (
  <div className="grid">
    {cells.map((c, i) => {
      let cls = 'pending';
      if (c.done) {
        if (i >= TARGET) cls = 'bonus';
        else if (c.doneToday) cls = 'today';
        else cls = 'done';
      }
      return (
        <div key={i} className={`cell ${cls}`} onClick={() => onCellClick && onCellClick(i)}>
          {i + 1}
        </div>
      );
    })}
  </div>
);

const SubtaskItem = ({ subtask, open, onToggle, onAddProgress, onDelete }) => {
  const doneCount = subtask.cells.filter(c => c.done).length;
  const pct = Math.min((doneCount / TARGET) * 100, 100);
  return (
    <div className={`subtask-item ${open ? 'open' : ''}`}>
      <div className="subtask-header" onClick={onToggle}>
        <span className="subtask-name">{subtask.name}</span>
        <div className="subtask-meta">
          <span>{doneCount}/{TARGET}</span>
          <div className="subtask-progress-wrap"><div className="subtask-progress-fill" style={{ width: `${pct}%` }} /></div>
        </div>
        <svg className="subtask-arrow" viewBox="0 0 20 20" fill="none">
          <path d="M5 8l5 5 5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      <div className="subtask-body">
        <div className="subtask-body-inner">
          <CellGrid cells={subtask.cells} onCellClick={() => onAddProgress()} />
          <button className="delete-subtask-btn" onClick={onDelete}>删除此子任务</button>
        </div>
      </div>
    </div>
  );
};

const TaskCard = ({ task, open, onToggle, onAddSubtask, onAddProgress, onDeleteTask, onDeleteSubtask }) => {
  const [openSubs, setOpenSubs] = React.useState({});
  const subtasks = task.subtasks || [];
  let totalDone = 0, totalToday = 0, totalBonus = 0;
  subtasks.forEach(st => st.cells.forEach((c, ci) => {
    if (c.done) { totalDone++; if (ci >= TARGET) totalBonus++; if (c.doneToday) totalToday++; }
  }));
  const pct = Math.min((totalDone / TARGET) * 100, 100);

  return (
    <div className={`task-card ${open ? 'open' : ''}`}>
      <div className="task-header" onClick={onToggle}>
        <div className="task-info">
          <div className="task-name">{task.name}</div>
          <div className="task-meta">
            <span>{totalDone} / {TARGET}</span>
            <div className="progress-bar-wrap"><div className="progress-bar-fill" style={{ width: `${pct}%` }} /></div>
            {totalToday > 0 && <span style={{ color: 'var(--yellow)' }}>●{totalToday}</span>}
            {totalBonus > 0 && <span style={{ color: 'var(--purple)' }}>+{totalBonus}</span>}
            <span style={{ color: 'var(--text-secondary)' }}>{subtasks.length} 个子任务</span>
          </div>
        </div>
        <svg className="task-arrow" viewBox="0 0 20 20" fill="none">
          <path d="M5 8l5 5 5-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
      </div>
      <div className="task-body">
        <div className="task-body-inner">
          <Legend />
          <div className="subtasks-section">
            {subtasks.map((st, si) => (
              <SubtaskItem
                key={si}
                subtask={st}
                open={!!openSubs[si]}
                onToggle={() => setOpenSubs(s => ({ ...s, [si]: !s[si] }))}
                onAddProgress={() => onAddProgress(si)}
                onDelete={() => onDeleteSubtask(si)}
              />
            ))}
          </div>
          <button className="add-subtask-btn" onClick={onAddSubtask}>+ 添加子任务</button>
          <button className="delete-task-btn" onClick={onDeleteTask}>删除任务</button>
        </div>
      </div>
    </div>
  );
};

window.TaskCard = TaskCard;
window.TARGET = TARGET;

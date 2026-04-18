// Calendar.jsx — month grid with today/selected/dot states
const WEEKDAYS = ['日', '一', '二', '三', '四', '五', '六'];

const Calendar = ({ year, month, today, selected, dotDates = new Set(), onPrev, onNext, onSelect }) => {
  const firstDay = new Date(year, month, 1).getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const prevDays = new Date(year, month, 0).getDate();

  const cells = [];
  for (let i = firstDay - 1; i >= 0; i--) {
    cells.push({ key: `p${i}`, label: prevDays - i, other: true });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
    cells.push({
      key: dateStr,
      label: d,
      isToday: dateStr === today,
      isSelected: dateStr === selected,
      hasDot: dotDates.has(dateStr),
      dateStr,
    });
  }
  const remaining = (7 - (cells.length % 7)) % 7;
  for (let i = 1; i <= remaining; i++) {
    cells.push({ key: `n${i}`, label: i, other: true });
  }

  return (
    <>
      <div className="calendar-header">
        <button className="cal-nav" onClick={onPrev}>◀</button>
        <h2>{year}年{month + 1}月</h2>
        <button className="cal-nav" onClick={onNext}>▶</button>
      </div>
      <div className="cal-weekdays">
        {WEEKDAYS.map((w) => <div key={w}>{w}</div>)}
      </div>
      <div className="cal-days">
        {cells.map(c => (
          <div
            key={c.key}
            className={`cal-day ${c.other ? 'other-month' : ''} ${c.isToday ? 'today' : ''} ${c.isSelected ? 'selected' : ''}`}
            onClick={() => !c.other && onSelect && onSelect(c.dateStr)}
          >
            {c.label}
            {c.hasDot && <div className="dot" />}
          </div>
        ))}
      </div>
    </>
  );
};

window.Calendar = Calendar;

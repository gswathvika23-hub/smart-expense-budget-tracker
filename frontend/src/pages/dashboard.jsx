import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "../api/axiosConfig";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

const COLORS = ["#6366F1", "#22C55E", "#F59E0B", "#EF4444"];

export default function Dashboard() {
  const [expenses, setExpenses] = useState([]);
  const [budgetStatus, setBudgetStatus] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }

    Promise.all([
      axios.get("/expenses"),
      axios.get("/budgets/status"),
    ])
      .then(([expensesRes, budgetRes]) => {
        setExpenses(expensesRes.data);
        setBudgetStatus(budgetRes.data);
      })
      .catch((err) => {
        console.error(err);
        setError("Failed to load dashboard data.");
      })
      .finally(() => setLoading(false));
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  const categoryTotals = expenses.reduce((acc, exp) => {
    const name = exp.category_name || exp.category || "Uncategorized";
    acc[name] = (acc[name] || 0) + Number(exp.amount);
    return acc;
  }, {});
  const chartData = Object.entries(categoryTotals).map(([name, value]) => ({
    name,
    value,
  }));

  if (loading) return <div style={{ padding: 24 }}>Loading dashboard...</div>;

  return (
    <div style={{ padding: 24, maxWidth: 900, margin: "0 auto" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1>Dashboard</h1>
        <button onClick={handleLogout}>Log out</button>
      </div>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <section style={{ margin: "24px 0" }}>
        <h2>Spending by Category</h2>
        {chartData.length === 0 ? (
          <p>No expenses yet — add one to see your breakdown.</p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={chartData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label
              >
                {chartData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )}
      </section>

      <section style={{ margin: "24px 0" }}>
        <h2>Budget Status</h2>
        {budgetStatus.length === 0 ? (
          <p>No budgets set yet.</p>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={{ textAlign: "left" }}>Category</th>
                <th>Limit</th>
                <th>Spent</th>
                <th>Remaining</th>
                <th>% Used</th>
              </tr>
            </thead>
            <tbody>
              {budgetStatus.map((b, i) => (
                <tr key={i}>
                  <td>{b.category_name || b.category_id}</td>
                  <td>{b.monthly_limit}</td>
                  <td>{b.spent}</td>
                  <td>{b.remaining}</td>
                  <td>{b.percent_used}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section style={{ margin: "24px 0" }}>
        <h2>Recent Expenses</h2>
        {expenses.length === 0 ? (
          <p>No expenses yet.</p>
        ) : (
          <ul>
            {expenses.slice(0, 10).map((exp) => (
              <li key={exp.id}>
                {exp.date} — {exp.description} — ₹{exp.amount} (
                {exp.category_name || exp.category_id})
              </li>
            ))}
          </ul>
        )}
      </section>
    </div>
  );
}
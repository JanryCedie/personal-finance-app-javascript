import React, { useState } from 'react';
import TransactionForm from './components/TransactionForm';
import WeeklyReport from './components/WeeklyReport';
import BreakdownChart from './components/BreakdownChart';
import TransactionList from './components/TransactionList';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleTransactionAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 tracking-tight sm:text-5xl">
            My Finance Tracker
          </h1>
          <p className="mt-4 text-lg text-gray-500">
            Track your income and expenses effortlessly.
          </p>
        </div>

        {/* Top Row: Form and Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
          {/* Left: Input Form */}
          <div className="lg:col-span-1 space-y-8">
            <TransactionForm onTransactionAdded={handleTransactionAdded} />
            <div className="bg-blue-50 p-6 rounded-2xl border border-blue-100">
              <h3 className="text-lg font-semibold text-blue-800 mb-2">Pro Tip</h3>
              <p className="text-blue-600 text-sm">
                Consistent tracking helps you save more. Try to add transactions daily!
              </p>
            </div>
          </div>

          {/* Middle: Weekly Report */}
          <div className="lg:col-span-1 h-full">
            <WeeklyReport refreshTrigger={refreshTrigger} />
          </div>

          {/* Right: Breakdown Pie Chart */}
          <div className="lg:col-span-1 h-full">
            <BreakdownChart refreshTrigger={refreshTrigger} />
          </div>
        </div>

        {/* Bottom Row: Transaction List */}
        <div className="w-full">
          <TransactionList
            refreshTrigger={refreshTrigger}
            onTransactionDeleted={handleTransactionAdded}
          />
        </div>

        <div className="mt-12 text-center text-gray-400 text-sm">
          &copy; {new Date().getFullYear()} Personal Finance App. Built with FastAPI & React.
        </div>
      </div>
    </div>
  );
}

export default App;

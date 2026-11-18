import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';

// Route-level code splitting via dynamic imports (Vercel React Best Practices)
const Home = lazy(() => import('./pages/Home').then((m) => ({ default: m.Home })));
const Login = lazy(() => import('./pages/Login').then((m) => ({ default: m.Login })));
const Register = lazy(() => import('./pages/Register').then((m) => ({ default: m.Register })));
const Assessment = lazy(() => import('./pages/Assessment').then((m) => ({ default: m.Assessment })));
const Results = lazy(() => import('./pages/Results').then((m) => ({ default: m.Results })));
const Dashboard = lazy(() => import('./pages/Dashboard').then((m) => ({ default: m.Dashboard })));
const Benchmarks = lazy(() => import('./pages/Benchmarks').then((m) => ({ default: m.Benchmarks })));
const ReportView = lazy(() => import('./pages/ReportView').then((m) => ({ default: m.ReportView })));

// Fluid skeleton loading boundary
const PageLoader = () => (
  <div className="min-h-[70dvh] flex flex-col items-center justify-center p-6 space-y-4">
    <div className="relative">
      <div className="w-12 h-12 rounded-2xl bg-indigo-600/20 border border-indigo-500/30 flex items-center justify-center animate-pulse">
        <div className="w-6 h-6 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin"></div>
      </div>
    </div>
    <span className="text-xs font-mono text-slate-400 tracking-wider uppercase">Loading View...</span>
  </div>
);

export function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="flex flex-col min-h-[100dvh] bg-slate-950 text-slate-100 overflow-x-hidden selection:bg-indigo-500/30 selection:text-indigo-200">
          <Navbar />
          <main className="flex-1 w-full max-w-full">
            <Suspense fallback={<PageLoader />}>
              <Routes>
                {/* Public Routes */}
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/benchmarks" element={<Benchmarks />} />

                {/* Protected Assessment & Dashboard Routes */}
                <Route
                  path="/assessment"
                  element={
                    <ProtectedRoute>
                      <Assessment />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/results"
                  element={
                    <ProtectedRoute>
                      <Results />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/dashboard"
                  element={
                    <ProtectedRoute>
                      <Dashboard />
                    </ProtectedRoute>
                  }
                />
                <Route
                  path="/report/:id"
                  element={
                    <ProtectedRoute>
                      <ReportView />
                    </ProtectedRoute>
                  }
                />

                {/* Fallback */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </Suspense>
          </main>
          <Footer />
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

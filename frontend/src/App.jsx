import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/layout/Navbar';
import ProtectedRoute from './components/layout/ProtectedRoute';

// Pages
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import CourseListPage from './pages/learn/CourseListPage';
import LessonPage from './pages/learn/LessonPage';
import CircuitBuilderPage from './pages/build/CircuitBuilderPage';
import SimulationResultsPage from './pages/results/SimulationResultsPage';
import AssessmentPage from './pages/assess/AssessmentPage';
import ProgressPage from './pages/progress/ProgressPage';
import CohortDashboardPage from './pages/instructor/CohortDashboardPage';
import ContentManagerPage from './pages/instructor/ContentManagerPage';

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          
          <Route path="/" element={<ProtectedRoute><CourseListPage /></ProtectedRoute>} />
          <Route path="/learn" element={<ProtectedRoute><CourseListPage /></ProtectedRoute>} />
          <Route path="/learn/lesson/:lessonId" element={<ProtectedRoute><LessonPage /></ProtectedRoute>} />
          
          <Route path="/build" element={<ProtectedRoute><CircuitBuilderPage /></ProtectedRoute>} />
          <Route path="/build/:circuitId" element={<ProtectedRoute><CircuitBuilderPage /></ProtectedRoute>} />
          
          <Route path="/results/:jobId" element={<ProtectedRoute><SimulationResultsPage /></ProtectedRoute>} />
          <Route path="/assess/:assessmentId" element={<ProtectedRoute><AssessmentPage /></ProtectedRoute>} />
          <Route path="/progress" element={<ProtectedRoute><ProgressPage /></ProtectedRoute>} />
          
          <Route path="/instructor" element={<ProtectedRoute roles={['instructor']}><CohortDashboardPage /></ProtectedRoute>} />
          <Route path="/instructor/content" element={<ProtectedRoute roles={['instructor']}><ContentManagerPage /></ProtectedRoute>} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Card from '../../components/ui/Card';
import Badge from '../../components/ui/Badge';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import * as coursesApi from '../../api/courses';
import { formatPercentage } from '../../utils/format';

const CourseListPage = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const data = await coursesApi.getCourses();
        // Placeholder data if api fails or is empty
        setCourses(data.length ? data : [
          { id: 1, title: 'Introduction to Quantum Computing', description: 'Learn the basics of qubits, superposition, and entanglement.', moduleCount: 5, progress: 0.2 },
          { id: 2, title: 'Quantum Algorithms', description: 'Deep dive into Grover\'s, Shor\'s and other famous algorithms.', moduleCount: 8, progress: 0 },
        ]);
      } catch (err) {
        console.error('Failed to load courses', err);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  const filteredCourses = courses.filter(c => c.title.toLowerCase().includes(search.toLowerCase()));

  if (loading) return <LoadingSpinner label="Loading courses..." />;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Learn</h1>
        <input
          type="text"
          placeholder="Search courses..."
          className="px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-md dark:bg-gray-800 dark:text-white"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCourses.map((course) => (
          <Link to={`/learn/lesson/${course.id}-1`} key={course.id}>
            <Card className="h-full hover:shadow-lg transition-shadow duration-200">
              <h2 className="text-xl font-semibold mb-2 text-gray-900 dark:text-white">{course.title}</h2>
              <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">{course.description}</p>
              
              <div className="flex items-center justify-between mb-4">
                <Badge variant="info">{course.moduleCount} Modules</Badge>
                <span className="text-sm text-gray-500 dark:text-gray-400">
                  {formatPercentage(course.progress)} Complete
                </span>
              </div>
              
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                <div 
                  className="bg-quantum-600 h-2.5 rounded-full" 
                  style={{ width: `${course.progress * 100}%` }}
                ></div>
              </div>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default CourseListPage;

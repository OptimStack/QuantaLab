import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import Card from '../../components/ui/Card';
import Button from '../../components/ui/Button';
import Badge from '../../components/ui/Badge';
import LoadingSpinner from '../../components/ui/LoadingSpinner';
import * as coursesApi from '../../api/courses';

const LessonPage = () => {
  const { lessonId } = useParams();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLesson = async () => {
      setLoading(true);
      try {
        // const data = await coursesApi.getLesson(lessonId);
        // Mock data
        setLesson({
          id: lessonId,
          title: 'Understanding Qubits',
          content: '## The Qubit\n\nUnlike classical bits which are 0 or 1, qubits can be in a superposition of both states.\n\n$$ |\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle $$',
          concepts: ['Superposition', 'Bloch Sphere'],
          estimatedTime: '15m',
        });
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchLesson();
  }, [lessonId]);

  if (loading) return <LoadingSpinner label="Loading lesson..." />;
  if (!lesson) return <div>Lesson not found</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex gap-6 h-[calc(100vh-4rem)]">
      <div className="flex-1 overflow-y-auto pr-4">
        <div className="mb-6 flex items-center justify-between">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">{lesson.title}</h1>
          <span className="text-sm text-gray-500 dark:text-gray-400">⏱ {lesson.estimatedTime}</span>
        </div>
        
        <div className="flex gap-2 mb-8">
          {lesson.concepts.map(concept => (
            <Badge key={concept} variant="info">{concept}</Badge>
          ))}
        </div>

        <div className="prose dark:prose-invert max-w-none mb-12">
          <ReactMarkdown>{lesson.content}</ReactMarkdown>
        </div>

        <div className="flex justify-between items-center border-t dark:border-gray-800 pt-6 mt-8">
          <Button variant="ghost">← Previous Lesson</Button>
          <Button>Mark Complete & Next →</Button>
        </div>
      </div>
      
      <div className="w-1/3 flex flex-col border-l border-gray-200 dark:border-gray-800 pl-6">
        <h3 className="font-semibold text-lg mb-4 dark:text-white">AI Tutor</h3>
        <Card className="flex-1 flex flex-col p-0 overflow-hidden bg-gray-50 dark:bg-gray-800">
          <div className="flex-1 p-4 overflow-y-auto">
            <div className="text-sm text-gray-500 text-center">Chat session started...</div>
            {/* Chat messages would go here */}
          </div>
          <div className="p-4 border-t dark:border-gray-700 bg-white dark:bg-gray-900">
            <input 
              type="text" 
              placeholder="Ask about this lesson..." 
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-1 focus:ring-quantum-500"
            />
          </div>
        </Card>
      </div>
    </div>
  );
};

export default LessonPage;

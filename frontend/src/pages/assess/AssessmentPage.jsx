import React from 'react';
import { useParams } from 'react-router-dom';
import Card from '../../components/ui/Card';

const AssessmentPage = () => {
  const { assessmentId } = useParams();

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Assessment {assessmentId}</h1>
      <Card>
        <p className="text-gray-600 dark:text-gray-300 mb-4">
          This is a placeholder for the AssessmentPage. It will route to QuizRunner or CodingChallengeRunner based on assessment type.
        </p>
      </Card>
    </div>
  );
};

export default AssessmentPage;

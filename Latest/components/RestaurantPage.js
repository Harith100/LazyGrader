"use client";

import React, { useState, useRef } from 'react';
import { Upload, FileText, Zap, ArrowRight, CheckCircle, Brain, Sparkles } from 'lucide-react';

const AIAnswerCorrectionSite = () => {
  const [currentPage, setCurrentPage] = useState('home');
  const [uploadedFiles, setUploadedFiles] = useState({
    answers: null,
    answerKey: null,
    questions: null
  });
  const [isProcessing, setIsProcessing] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [correctionResults, setCorrectionResults] = useState(null);
  const [error, setError] = useState(null);

  const fileInputRefs = {
    answers: useRef(null),
    answerKey: useRef(null),
    questions: useRef(null)
  };

  const handleFileUpload = (type, event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setUploadedFiles(prev => ({
        ...prev,
        [type]: file
      }));
      setError(null); // Clear any previous errors
    }
  };

  const handleAICorrection = async () => {
    if (uploadedFiles.answers && uploadedFiles.answerKey && uploadedFiles.questions) {
      setIsProcessing(true);
      setError(null);

      try {
        // Create FormData to send files
        const formData = new FormData();
        formData.append('answers', uploadedFiles.answers);
        formData.append('answer_key', uploadedFiles.answerKey);
        formData.append('questions', uploadedFiles.questions);

        // Send request to FastAPI backend
        const response = await fetch('http://localhost:8000/correct-answers', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const results = await response.json();
        setCorrectionResults(results);
        setShowResults(true);
      } catch (error) {
        console.error('Error processing correction:', error);
        setError('Failed to process correction. Please ensure the FastAPI server is running on localhost:8000');
      } finally {
        setIsProcessing(false);
      }
    }
  };

  const resetDemo = () => {
    setUploadedFiles({
      answers: null,
      answerKey: null,
      questions: null
    });
    setShowResults(false);
    setIsProcessing(false);
    setCorrectionResults(null);
    setError(null);
  };

  if (currentPage === 'home') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100">
        {/* Navigation */}
        <nav className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50">
          <div className="max-w-7xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <Brain className="w-8 h-8 text-blue-600" />
                <span className="text-xl font-semibold text-gray-900">AI Corrector</span>
              </div>
              <button
                onClick={() => setCurrentPage('demo')}
                className="px-6 py-2 bg-blue-600 text-white rounded-full hover:bg-blue-700 transition-all duration-300 font-medium"
              >
                Try Demo
              </button>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <div className="pt-32 pb-20">
          <div className="max-w-6xl mx-auto px-6 text-center">
            <div className="inline-flex items-center px-4 py-2 bg-blue-50 text-blue-700 rounded-full text-sm font-medium mb-8">
              <Sparkles className="w-4 h-4 mr-2" />
              AI-Powered Answer Correction
            </div>
            
            <h1 className="text-6xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
              Intelligent
              <br />
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Answer Correction
              </span>
            </h1>
            
            <p className="text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed">
              Experience the future of automated grading with our advanced AI model. 
              Upload your PDFs and let artificial intelligence provide precise, 
              instant corrections with detailed insights.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <button
                onClick={() => setCurrentPage('demo')}
                className="group px-8 py-4 bg-blue-600 text-white rounded-2xl hover:bg-blue-700 transition-all duration-300 font-semibold text-lg flex items-center shadow-xl hover:shadow-2xl transform hover:-translate-y-1"
              >
                Get Started
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </button>
              <button className="px-8 py-4 border-2 border-gray-300 text-gray-700 rounded-2xl hover:border-blue-600 hover:text-blue-600 transition-all duration-300 font-semibold text-lg">
                Learn More
              </button>
            </div>
          </div>
        </div>

        {/* Features */}
        <div className="py-20 bg-white">
          <div className="max-w-6xl mx-auto px-6">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Why Choose AI Corrector?
              </h2>
              <p className="text-xl text-gray-600">
                Built with cutting-edge technology for unparalleled accuracy
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8">
              {[
                {
                  icon: <Zap className="w-8 h-8 text-blue-600" />,
                  title: "Lightning Fast",
                  description: "Process hundreds of answers in seconds with our optimized AI engine"
                },
                {
                  icon: <Brain className="w-8 h-8 text-purple-600" />,
                  title: "Intelligent Analysis",
                  description: "Advanced natural language processing for nuanced answer evaluation"
                },
                {
                  icon: <CheckCircle className="w-8 h-8 text-green-600" />,
                  title: "Precise Results",
                  description: "Industry-leading accuracy with detailed feedback and scoring"
                }
              ].map((feature, index) => (
                <div key={index} className="group p-8 bg-gray-50 rounded-3xl hover:bg-white hover:shadow-xl transition-all duration-300 border border-gray-100">
                  <div className="mb-4">{feature.icon}</div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">{feature.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => setCurrentPage('home')}
              className="flex items-center space-x-2 hover:opacity-80 transition-opacity"
            >
              <Brain className="w-8 h-8 text-blue-600" />
              <span className="text-xl font-semibold text-gray-900">AI Corrector</span>
            </button>
            <button
              onClick={resetDemo}
              className="px-6 py-2 bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-all duration-300 font-medium"
            >
              Reset Demo
            </button>
          </div>
        </div>
      </nav>

      <div className="pt-24 pb-12">
        <div className="max-w-6xl mx-auto px-6">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              AI Correction Demo
            </h1>
            <p className="text-lg text-gray-600">
              Upload your PDF files and experience the power of AI-driven answer correction
            </p>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl">
              <p className="text-red-700">{error}</p>
            </div>
          )}

          {isProcessing ? (
            /* Loading Animation */
            <div className="flex flex-col items-center justify-center py-20">
              <div className="relative">
                <div className="w-32 h-32 border-8 border-blue-100 rounded-full"></div>
                <div className="absolute top-0 left-0 w-32 h-32 border-8 border-blue-600 rounded-full border-t-transparent animate-spin"></div>
                <div className="absolute top-4 left-4 w-24 h-24 border-4 border-purple-200 rounded-full"></div>
                <div className="absolute top-4 left-4 w-24 h-24 border-4 border-purple-600 rounded-full border-t-transparent animate-spin" style={{animationDirection: 'reverse', animationDuration: '3s'}}></div>
                <Brain className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-12 h-12 text-blue-600 animate-pulse" />
              </div>
              <div className="mt-8 text-center">
                <h3 className="text-2xl font-semibold text-gray-900 mb-2">
                  AI is Processing...
                </h3>
                <p className="text-gray-600">
                  Analyzing answers with advanced machine learning algorithms
                </p>
                <div className="flex justify-center mt-4 space-x-1">
                  {[0, 1, 2].map((i) => (
                    <div
                      key={i}
                      className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"
                      style={{animationDelay: `${i * 0.1}s`}}
                    ></div>
                  ))}
                </div>
              </div>
            </div>
          ) : showResults && correctionResults ? (
            /* Results */
            <div className="bg-white rounded-3xl shadow-xl p-8 border border-gray-100">
              <div className="text-center mb-8">
                <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                  Correction Complete!
                </h2>
                <p className="text-gray-600">
                  Your answers have been analyzed and corrected
                </p>
              </div>

              <div className="grid md:grid-cols-2 gap-6 mb-8">
                <div className="bg-green-50 p-6 rounded-2xl border border-green-200">
                  <h3 className="text-lg font-semibold text-green-800 mb-2">Overall Score</h3>
                  <div className="text-3xl font-bold text-green-600">{correctionResults.overall_score}%</div>
                  <p className="text-green-700 text-sm">{correctionResults.performance_message}</p>
                </div>
                <div className="bg-blue-50 p-6 rounded-2xl border border-blue-200">
                  <h3 className="text-lg font-semibold text-blue-800 mb-2">Questions Analyzed</h3>
                  <div className="text-3xl font-bold text-blue-600">{correctionResults.total_questions}</div>
                  <p className="text-blue-700 text-sm">All questions processed</p>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-gray-900">Detailed Feedback</h3>
                {correctionResults.detailed_feedback.map((item, index) => (
                  <div key={index} className="bg-gray-50 p-4 rounded-xl border border-gray-200">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium text-gray-900">{item.question}</span>
                      <span className="text-blue-600 font-semibold">{item.score}%</span>
                    </div>
                    <p className="text-gray-600 text-sm">{item.feedback}</p>
                  </div>
                ))}
              </div>
            </div>
          ) : (
            /* Upload Interface */
            <div className="space-y-8">
              {/* File Upload Cards */}
              <div className="grid lg:grid-cols-3 gap-6">
                {[
                  { key: 'answers', label: 'Student Answers', icon: FileText, color: 'blue' },
                  { key: 'answerKey', label: 'Answer Key', icon: CheckCircle, color: 'green' },
                  { key: 'questions', label: 'Questions', icon: Upload, color: 'purple' }
                ].map((item) => (
                  <div key={item.key} className="group">
                    <div 
                      className={`relative bg-white rounded-3xl p-8 border-2 border-dashed transition-all duration-300 hover:shadow-lg cursor-pointer ${
                        uploadedFiles[item.key] 
                          ? `border-${item.color}-500 bg-${item.color}-50` 
                          : 'border-gray-300 hover:border-gray-400'
                      }`}
                      onClick={() => fileInputRefs[item.key].current?.click()}
                    >
                      <input
                        ref={fileInputRefs[item.key]}
                        type="file"
                        accept=".pdf"
                        onChange={(e) => handleFileUpload(item.key, e)}
                        className="hidden"
                      />
                      
                      <div className="text-center">
                        <item.icon className={`w-12 h-12 mx-auto mb-4 ${
                          uploadedFiles[item.key] ? `text-${item.color}-600` : 'text-gray-400'
                        }`} />
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">
                          {item.label}
                        </h3>
                        
                        {uploadedFiles[item.key] ? (
                          <div className={`text-${item.color}-600 font-medium`}>
                            ✓ {uploadedFiles[item.key].name}
                          </div>
                        ) : (
                          <div className="text-gray-500">
                            <p className="mb-2">Click to upload PDF</p>
                            <div className="inline-flex items-center px-4 py-2 bg-gray-100 rounded-full text-sm">
                              <Upload className="w-4 h-4 mr-2" />
                              Choose file
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Action Button */}
              <div className="text-center">
                <button
                  onClick={handleAICorrection}
                  disabled={!uploadedFiles.answers || !uploadedFiles.answerKey || !uploadedFiles.questions}
                  className={`group px-12 py-4 rounded-2xl font-semibold text-lg transition-all duration-300 flex items-center mx-auto ${
                    uploadedFiles.answers && uploadedFiles.answerKey && uploadedFiles.questions
                      ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-xl hover:shadow-2xl transform hover:-translate-y-1'
                      : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  <Zap className="w-6 h-6 mr-3 group-hover:animate-pulse" />
                  Start AI Correction
                </button>
                
                {(!uploadedFiles.answers || !uploadedFiles.answerKey || !uploadedFiles.questions) && (
                  <p className="text-gray-500 mt-4 text-sm">
                    Please upload all three PDF files to proceed
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIAnswerCorrectionSite;
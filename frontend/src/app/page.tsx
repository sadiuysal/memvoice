export default function HomePage() {
  return (
    <main className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to MemVoice
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Memory-Optimized Voice Agent Pipeline
          </p>
          <div className="bg-white rounded-lg shadow-md p-6 max-w-2xl mx-auto">
            <h2 className="text-2xl font-semibold mb-4">
              Development Environment
            </h2>
            <p className="text-gray-700 mb-4">
              Your MemVoice development environment is running successfully!
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
              <div className="bg-green-50 p-3 rounded">
                <h3 className="font-semibold text-green-800">Frontend</h3>
                <p className="text-green-600">
                  Next.js app running on port 3000
                </p>
              </div>
              <div className="bg-blue-50 p-3 rounded">
                <h3 className="font-semibold text-blue-800">Backend</h3>
                <p className="text-blue-600">FastAPI server on port 8000</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

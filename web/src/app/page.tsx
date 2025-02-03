import TaskList from "@/components/TaskList";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-8">
      <main className="container mx-auto">
        <TaskList />
      </main>
    </div>
  );
}

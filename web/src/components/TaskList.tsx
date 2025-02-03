'use client';

import { useState } from 'react';

interface Task {
    id: number;
    title: string;
    completed: boolean;
}

export default function TaskList() {
    const [tasks, setTasks] = useState<Task[]>([
        { id: 1, title: "Next.jsの学習", completed: false },
        { id: 2, title: "TypeScriptの練習", completed: true },
        { id: 3, title: "TailwindCSSの実践", completed: false },
    ]);

    const toggleTask = (id: number) => {
        setTasks(tasks.map(task =>
            task.id === id ? { ...task, completed: !task.completed } : task
        ));
    };

    return (
        <div className="w-full max-w-md mx-auto">
            <h1 className="text-2xl font-bold mb-4">タスク一覧</h1>
            <ul className="space-y-2">
                {tasks.map(task => (
                    <li
                        key={task.id}
                        className="flex items-center p-3 bg-white dark:bg-gray-800 rounded-lg shadow hover:shadow-md transition-shadow"
                    >
                        <label className="flex items-center w-full cursor-pointer">
                            <input
                                type="checkbox"
                                checked={task.completed}
                                onChange={() => toggleTask(task.id)}
                                className="w-4 h-4 mr-3 rounded border-gray-300"
                                aria-label={`タスク「${task.title}」を${task.completed ? '未完了' : '完了'}としてマーク`}
                            />
                            <span className={`flex-1 ${task.completed ? 'line-through text-gray-500' : ''}`}>
                                {task.title}
                            </span>
                        </label>
                    </li>
                ))}
            </ul>
        </div>
    );
}

"use client";

import { useEffect, useState } from "react";

type DashboardStats = {
  total_bookings: number;
  total_revenue: number;
};

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStats() {
      try {
        const token = localStorage.getItem("admin_token");

        if (!token) {
          throw new Error("Unauthorized");
        }

        const res = await fetch("/api/v1/admin/analytics", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!res.ok) {
          throw new Error("Failed to fetch dashboard data");
        }

        const data = await res.json();
        setStats(data);
      } catch (err: any) {
        setError(err.message || "Something went wrong");
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
  }, []);

  if (loading) {
    return <div className="p-8">Loading dashboard...</div>;
  }

  if (error) {
    return (
      <div className="p-8 text-red-600">
        {error}
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-semibold mb-8">
        Admin Dashboard
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Total Bookings */}
        <div className="rounded-xl border p-6 shadow-sm">
          <h2 className="text-sm text-gray-500 mb-2">
            Total Bookings
          </h2>
          <p className="text-3xl font-bold">
            {stats.total_bookings}
          </p>
        </div>

        {/* Total Revenue */}
        <div className="rounded-xl border p-6 shadow-sm">
          <h2 className="text-sm text-gray-500 mb-2">
            Total Revenue
          </h2>
          <p className="text-3xl font-bold">
            ₹{stats.total_revenue}
          </p>
        </div>
      </div>

      {/* Quick Links */}
      <div className="mt-10">
        <h2 className="text-xl font-medium mb-4">
          Quick Actions
        </h2>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <a
            href="/admin/bookings"
            className="border rounded-lg p-4 text-center hover:bg-gray-50 transition"
          >
            Manage Bookings
          </a>

          <a
            href="/admin/rooms"
            className="border rounded-lg p-4 text-center hover:bg-gray-50 transition"
          >
            Manage Rooms
          </a>

          <a
            href="/admin/pricing"
            className="border rounded-lg p-4 text-center hover:bg-gray-50 transition"
          >
            Pricing Rules
          </a>

          <a
            href="/admin/reviews"
            className="border rounded-lg p-4 text-center hover:bg-gray-50 transition"
          >
            Reviews
          </a>
        </div>
      </div>
    </div>
  );
}

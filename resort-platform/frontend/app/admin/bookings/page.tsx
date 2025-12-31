"use client";

import { useEffect, useState } from "react";

type Room = {
  id: number;
  name: string;
  base_price: number;
  max_adults: number;
  max_children: number;
};

export default function BookingsPage() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const [form, setForm] = useState({
    room_id: "",
    guest_name: "",
    guest_email: "",
    guest_phone: "",
    check_in: "",
    check_out: "",
    adults: 2,
    children: 0,
    special_requests: "",
  });

  const [estimatedTotal, setEstimatedTotal] = useState<number>(0);

  // --------------------------------------------
  // Fetch rooms
  // --------------------------------------------
  useEffect(() => {
    async function fetchRooms() {
      try {
        const res = await fetch("/api/v1/rooms");
        const data = await res.json();
        setRooms(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchRooms();
  }, []);

  // --------------------------------------------
  // Estimate total (basic client-side)
  // --------------------------------------------
  useEffect(() => {
    const room = rooms.find(r => r.id === Number(form.room_id));
    if (!room || !form.check_in || !form.check_out) {
      setEstimatedTotal(0);
      return;
    }

    const start = new Date(form.check_in);
    const end = new Date(form.check_out);
    const nights =
      (end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24);

    if (nights > 0) {
      setEstimatedTotal(nights * room.base_price);
    } else {
      setEstimatedTotal(0);
    }
  }, [form, rooms]);

  // --------------------------------------------
  // Handlers
  // --------------------------------------------
  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    setMessage(null);

    try {
      const res = await fetch("/api/v1/bookings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ...form,
          room_id: Number(form.room_id),
          adults: Number(form.adults),
          children: Number(form.children),
          total_amount: estimatedTotal,
        }),
      });

      if (!res.ok) {
        throw new Error("Booking failed");
      }

      setMessage("Booking confirmed! We will contact you shortly.");
      setForm({
        room_id: "",
        guest_name: "",
        guest_email: "",
        guest_phone: "",
        check_in: "",
        check_out: "",
        adults: 2,
        children: 0,
        special_requests: "",
      });
      setEstimatedTotal(0);
    } catch (err) {
      setMessage("Unable to complete booking. Please try again.");
    } finally {
      setSubmitting(false);
    }
  }

  // --------------------------------------------
  // Render
  // --------------------------------------------
  if (loading) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-semibold mb-6">Book Your Stay</h1>

      <form onSubmit={handleSubmit} className="space-y-5">
        <select
          name="room_id"
          value={form.room_id}
          onChange={handleChange}
          required
          className="w-full border rounded px-3 py-2"
        >
          <option value="">Select Room</option>
          {rooms.map(room => (
            <option key={room.id} value={room.id}>
              {room.name} – ₹{room.base_price}/night
            </option>
          ))}
        </select>

        <input
          name="guest_name"
          placeholder="Full Name"
          value={form.guest_name}
          onChange={handleChange}
          required
          className="w-full border rounded px-3 py-2"
        />

        <input
          name="guest_email"
          type="email"
          placeholder="Email"
          value={form.guest_email}
          onChange={handleChange}
          required
          className="w-full border rounded px-3 py-2"
        />

        <input
          name="guest_phone"
          placeholder="Phone Number"
          value={form.guest_phone}
          onChange={handleChange}
          required
          className="w-full border rounded px-3 py-2"
        />

        <div className="grid grid-cols-2 gap-4">
          <input
            type="date"
            name="check_in"
            value={form.check_in}
            onChange={handleChange}
            required
            className="border rounded px-3 py-2"
          />
          <input
            type="date"
            name="check_out"
            value={form.check_out}
            onChange={handleChange}
            required
            className="border rounded px-3 py-2"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <input
            type="number"
            name="adults"
            min={1}
            value={form.adults}
            onChange={handleChange}
            className="border rounded px-3 py-2"
          />
          <input
            type="number"
            name="children"
            min={0}
            value={form.children}
            onChange={handleChange}
            className="border rounded px-3 py-2"
          />
        </div>

        <textarea
          name="special_requests"
          placeholder="Special Requests (optional)"
          value={form.special_requests}
          onChange={handleChange}
          className="w-full border rounded px-3 py-2"
        />

        <div className="text-right font-medium">
          Estimated Total: ₹{estimatedTotal}
        </div>

        <button
          type="submit"
          disabled={submitting}
          className="w-full bg-black text-white py-3 rounded hover:bg-gray-800 transition"
        >
          {submitting ? "Booking..." : "Confirm Booking"}
        </button>

        {message && (
          <p className="text-center text-sm text-gray-700">{message}</p>
        )}
      </form>
    </div>
  );
}

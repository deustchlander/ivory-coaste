"use client";

import { useEffect, useState } from "react";

type Room = {
  id: number;
  name: string;
};

type PricingResponse = {
  room_id: number;
  check_in: string;
  check_out: string;
  total_price: number;
  currency: string;
};

export default function PricingPage() {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [roomId, setRoomId] = useState("");
  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [pricing, setPricing] = useState<PricingResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // --------------------------------------------
  // Fetch rooms
  // --------------------------------------------
  useEffect(() => {
    async function fetchRooms() {
      try {
        const res = await fetch("/api/v1/rooms");
        const data = await res.json();
        setRooms(data);
      } catch {
        setError("Unable to load rooms");
      }
    }
    fetchRooms();
  }, []);

  // --------------------------------------------
  // Fetch pricing
  // --------------------------------------------
  async function handleCheckPrice() {
    if (!roomId || !checkIn || !checkOut) {
      setError("Please select room and dates");
      return;
    }

    setLoading(true);
    setError(null);
    setPricing(null);

    try {
      const res = await fetch(
        `/api/v1/pricing/room/${roomId}/price?check_in=${checkIn}&check_out=${checkOut}`
      );

      if (!res.ok) {
        throw new Error();
      }

      const data = await res.json();
      setPricing(data);
    } catch {
      setError("Unable to calculate price");
    } finally {
      setLoading(false);
    }
  }

  // --------------------------------------------
  // Render
  // --------------------------------------------
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-semibold mb-6">
        Pricing & Availability
      </h1>

      <div className="space-y-4 mb-6">
        <select
          value={roomId}
          onChange={(e) => setRoomId(e.target.value)}
          className="w-full border rounded px-3 py-2"
        >
          <option value="">Select Room</option>
          {rooms.map((room) => (
            <option key={room.id} value={room.id}>
              {room.name}
            </option>
          ))}
        </select>

        <div className="grid grid-cols-2 gap-4">
          <input
            type="date"
            value={checkIn}
            onChange={(e) => setCheckIn(e.target.value)}
            className="border rounded px-3 py-2"
          />
          <input
            type="date"
            value={checkOut}
            onChange={(e) => setCheckOut(e.target.value)}
            className="border rounded px-3 py-2"
          />
        </div>

        <button
          onClick={handleCheckPrice}
          disabled={loading}
          className="w-full bg-black text-white py-3 rounded hover:bg-gray-800 transition"
        >
          {loading ? "Calculating..." : "Check Price"}
        </button>
      </div>

      {error && (
        <p className="text-center text-red-600 mb-4">
          {error}
        </p>
      )}

      {pricing && (
        <div className="border rounded-lg p-6 text-center">
          <p className="text-sm text-gray-500 mb-2">
            Total Price
          </p>
          <p className="text-3xl font-bold">
            ₹{pricing.total_price}
          </p>
          <p className="text-sm text-gray-500 mt-1">
            For selected dates
          </p>
        </div>
      )}
    </div>
  );
}

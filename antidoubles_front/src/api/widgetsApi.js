import { BASE_URL, TOKEN } from "../config";

const API_BASE_URL = `${BASE_URL}/widgets`;

const headers = {
    Authorization: `Bearer ${TOKEN}`,
    'Content-Type': 'application/json',
};

export const getAllWidgets = async () => {
  const response = await fetch(API_BASE_URL, {
	headers: headers
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const getWidgetById = async (widgetId) => {
  const response = await fetch(`${API_BASE_URL}/${widgetId}`,{
	headers: headers
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const createWidget = async (widgetData) => {
  const response = await fetch(API_BASE_URL, {
    method: 'POST',
    headers,
    body: JSON.stringify(widgetData),
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const updateWidget = async (widgetId, widgetData) => {
  const response = await fetch(`${API_BASE_URL}/${widgetId}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(widgetData),
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return await response.json();
};

export const deleteWidget = async (widgetId) => {
  const response = await fetch(`${API_BASE_URL}/${widgetId}`, {
    method: 'DELETE',
    headers,
  });
  if (!response.ok) {
    throw new Error(`Ошибка: ${response.statusText}`);
  }
  return true;
};

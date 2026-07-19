export function getErrorMessage(err: any, fallback: string): string {
  const detail = err?.response?.data?.detail;

  if (!detail) return fallback;
  if (typeof detail === 'string') return detail;

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'string') return item;
        if (item?.msg) {
          const field = Array.isArray(item.loc) ? item.loc.at(-1) : '';
          return field ? `${field}: ${item.msg}` : item.msg;
        }
        return null;
      })
      .filter(Boolean)
      .join(' — ') || fallback;
  }

  return fallback;
}
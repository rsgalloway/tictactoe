export function iconPath(name: "tick" | "eyeball") {
  const dpr = (typeof window !== "undefined" ? Math.ceil(window.devicePixelRatio || 1) : 1);
  const scale = dpr >= 2 ? "2x" : "1x";
  return `/icons/${name}-${scale}.png`;
}
  
export const metadata = { title: "Engineering CAD Platform" };
export default function RootLayout({children}:{children:React.ReactNode}) {
  return <html lang="en"><body style={{margin:0,fontFamily:"Arial, sans-serif",background:"#f4f6f8"}}>{children}</body></html>
}

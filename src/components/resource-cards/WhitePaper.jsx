// app-white-paper (`_whitePaper_1tkgo`): rotated cover sheet + white back sheet + drop shadow.
export default function WhitePaper({ className = '', children }) {
  return (
    <div className={`wp ${className}`}>
      <div className="wp__A1">
        <div className="wp__B1">{children}</div>
      </div>
    </div>
  )
}

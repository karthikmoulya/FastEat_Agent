import { CameraIcon, LogoIcon } from './Icons.jsx'

export default function Header({ view, onHome }) {
  return (
    <header className="site-header">
      <div className={`site-header__inner ${view === 'cook' ? 'wide' : ''}`}>
        <button className="logo" onClick={onHome}>
          <span className="logo__mark"><LogoIcon stroke="var(--bg)" /></span>
          <span className="logo__text">FastEat</span>
        </button>
        {view === 'upload' ? (
          <nav aria-label="Main">
            <a className="nav-link" href="#how">How it works</a>
          </nav>
        ) : (
          <button className="btn btn--outline btn--small" onClick={onHome}>
            <CameraIcon size={16} /> New photo
          </button>
        )}
      </div>
    </header>
  )
}

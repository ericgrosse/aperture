import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

import {
  Home, Search, Bell, Mail, Bookmark, List, User, Plus,
  SlidersHorizontal, Heart, Repeat2, MessageCircle, Sparkles,
  ShieldCheck, Eye, Leaf, Info, Image as Img, MapPin,
  BarChart3, Settings, MoreHorizontal, X
} from 'lucide-react';

import './styles.css';

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const basePrefs = {
  meaningful: 65,
  intellectual: 65,
  original: 60,
  depth: 65,
  positivity: 80,
  slower_pace: 65,
  niche: 65,
  politics: 'show_less',
  outrage: 'show_less',
  reposts: 'show_less',
  sensitive: 'limit',
  sources: {
    following: 45,
    curated: 25,
    small_creators: 20,
    local: 10,
  },
};

const left = {
  meaningful: 'Meaningful',
  intellectual: 'Intellectual',
  original: 'Original',
  depth: 'Depth',
  positivity: 'Positivity',
  slower_pace: 'Slower pace',
  niche: 'Niche',
};

const right = {
  meaningful: 'Entertaining',
  intellectual: 'Lighthearted',
  original: 'Viral',
  depth: 'Surface',
  positivity: 'Edgy',
  slower_pace: 'Fast-paced',
  niche: 'Mainstream',
};

function App() {
  const [prefs, setPrefs] = useState(basePrefs);
  const [posts, setPosts] = useState([]);
  const [modes, setModes] = useState({});
  const [active, setActive] = useState('Deep Focus');
  const [text, setText] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  const rank = async (p = prefs) => {
    const response = await fetch(`${API}/api/feed/rank`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(p),
    });

    const data = await response.json();
    setPosts(data.posts || []);
  };

  useEffect(() => {
    fetch(`${API}/api/modes`)
      .then((r) => r.json())
      .then(setModes)
      .catch(() => {});

    rank();
  }, []);

  const update = (key, value) => {
    const next = {
      ...prefs,
      [key]: Number(value),
    };

    setPrefs(next);
    setActive('Custom Mode');
    rank(next);
  };

  const selectMode = (name) => {
    const next = {
      ...basePrefs,
      ...(modes[name] || {}),
    };

    setActive(name);
    setPrefs(next);
    rank(next);
  };

  const create = async () => {
    const trimmed = text.trim();

    if (!trimmed && !imageUrl) return;

    try {
      const response = await fetch(`${API}/api/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          text: trimmed || 'Shared an image.',
          author: 'Nova',
          handle: '@novasync',
          image_url: imageUrl || null,
          tags: ['aperture', 'user post'],
        }),
      });

      const data = await response.json();

      if (!response.ok || data.error) {
        console.error('Failed to create post:', data);
        alert(data.error || 'Failed to create post.');
        return;
      }

      const visiblePost = {
        ...data,
        rank_score: 'New',
        reasons: ['You just posted this.'],
      };

      setText('');
      setImageUrl('');
      setPosts((currentPosts) => [visiblePost, ...currentPosts]);
    } catch (error) {
      console.error('Post request failed:', error);
      alert('Could not connect to the backend.');
    }
  };

  return (
    <div className="app">
      <Sidebar active={active} selectMode={selectMode} />

      <main className="main">
        <Header active={active} />

        <Composer
          text={text}
          setText={setText}
          imageUrl={imageUrl}
          setImageUrl={setImageUrl}
          create={create}
        />

        {posts.map((post) => (
          <Post key={post.id} post={post} />
        ))}
      </main>

      <Controls
        prefs={prefs}
        update={update}
        setPrefs={setPrefs}
        rank={rank}
      />

      <MobileNav />
    </div>
  );
}

function Sidebar({ active, selectMode }) {
  const modes = [
    ['Default', 'Balanced discovery', Sparkles],
    ['Deep Focus', 'Low distraction', Eye],
    ['Creative Spark', 'Art, music, and ideas', Sparkles],
    ['Local Pulse', 'Community first', MapPin],
    ['Custom Mode', 'Edit preferences', SlidersHorizontal],
  ];

  return (
    <aside className="side">
      <div className="brand">
        <div className="orb"></div>
        <div>
          <b>Aperture</b>
          <span>Your feed. Your rules.</span>
        </div>
      </div>

      <nav>
        {[
          [Home, 'Home'],
          [Search, 'Explore'],
          [Bell, 'Notifications'],
          [Mail, 'Messages'],
          [Bookmark, 'Bookmarks'],
          [List, 'Lists'],
          [User, 'Profile'],
          [Plus, 'Create'],
        ].map(([Icon, title]) => (
          <a key={title}>
            <Icon size={21} />
            {title}
          </a>
        ))}
      </nav>

      <div className="modes">
        <div className="mode-title">
          FEED MODES <Plus size={16} />
        </div>

        {modes.map(([name, desc, Icon]) => (
          <button
            key={name}
            className={active === name ? 'mode on' : 'mode'}
            onClick={() => selectMode(name)}
          >
            <Icon size={18} />
            <span>
              <b>{name}</b>
              <small>{desc}</small>
            </span>
          </button>
        ))}
      </div>

      <div className="trust">
        <b>Why am I seeing this?</b>
        <span>Transparency builds trust.</span>
        <button>Learn more</button>
      </div>

      <div className="me">
        <div className="avatar">🧠</div>
        <div>
          Nova
          <br />
          <span>@novasync</span>
        </div>
        <MoreHorizontal size={16} />
      </div>
    </aside>
  );
}

function Header({ active }) {
  return (
    <>
      <header>
        <h1>Good morning, Nova 👋</h1>
        <p>
          You’re in {active} mode <button>Change</button>
        </p>
      </header>

      <section className="status">
        <Card icon={<ShieldCheck />} title="Feed Health" value="Excellent" />
        <Card icon={<Eye />} title="Algorithm Transparency" value="High" />
        <Card icon={<Leaf />} title="Personalization" value="Yours" />
      </section>
    </>
  );
}

function Card({ icon, title, value }) {
  return (
    <div className="status-card">
      <span>{icon}</span>
      <div>
        {title}
        <b>{value}</b>
      </div>
    </div>
  );
}

function Composer({ text, setText, imageUrl, setImageUrl, create }) {
  const handleImage = (event) => {
    const file = event.target.files?.[0];

    if (!file) return;

    if (!file.type.startsWith('image/')) {
      alert('Please choose an image file.');
      return;
    }

    const reader = new FileReader();

    reader.onload = () => {
      setImageUrl(reader.result);
    };

    reader.readAsDataURL(file);
  };

  return (
    <div className="composer">
      <div className="avatar">🧠</div>

      <div className="compose-body">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Share a thought..."
        />

        {imageUrl && (
          <div className="image-preview-wrap">
            <img className="image-preview" src={imageUrl} alt="Upload preview" />

            <button
              className="remove-image"
              type="button"
              onClick={() => setImageUrl('')}
              title="Remove image"
            >
              <X size={18} />
            </button>
          </div>
        )}

        <div className="compose-actions">
          <div className="compose-tools">
            <label className="upload-button">
              <Img size={20} />
              Add image
              <input type="file" accept="image/*" onChange={handleImage} />
            </label>

            <BarChart3 size={20} />
            <MapPin size={20} />
          </div>

          <button onClick={create}>Post</button>
        </div>
      </div>
    </div>
  );
}

function Post({ post }) {
  return (
    <article className="post">
      <div className="post-top">
        <div className="avatar">{post.avatar}</div>

        <div>
          <b>{post.author}</b>
          <span>
            {post.handle} · {timeAgo(post.created_at)}
          </span>
        </div>

        <button className="pill">✦ Original creator</button>

        <MoreHorizontal size={18} />
      </div>

      <p className="post-text">{post.text}</p>

      {post.image_url && (
        <img className="hero-img" src={post.image_url} alt="Post attachment" />
      )}

      <div className="metrics">
        <span>
          <MessageCircle /> {post.replies}
        </span>
        <span>
          <Repeat2 /> {post.reposts}
        </span>
        <span>
          <Heart /> {post.likes}
        </span>
        <span>
          <Bookmark />
        </span>
      </div>

      <div className="why">
        <div>
          <b>Why you’re seeing this</b>
          <small>Rank score: {post.rank_score}</small>
        </div>

        {post.reasons?.map((reason, i) => (
          <p key={i}>
            <Info size={14} />
            {reason}
          </p>
        ))}
      </div>
    </article>
  );
}

function Controls({ prefs, update, setPrefs, rank }) {
  const filters = ['politics', 'outrage', 'reposts', 'sensitive'];

  const labels = {
    politics: 'Politics',
    outrage: 'Outrage / Rage bait',
    reposts: 'Reposts / Memes',
    sensitive: 'Sensitive content',
  };

  const reset = () => {
    setPrefs(basePrefs);
    rank(basePrefs);
  };

  return (
    <aside className="controls">
      <div className="panel">
        <div className="panel-head">
          <h2>Algorithm Controls</h2>
          <button onClick={reset}>Reset</button>
        </div>

        <p>Fine-tune what you see. Your feed adapts in real time.</p>

        <div className="tabs">
          <b>Preferences</b>
          <span>Sources</span>
          <span>Behavior</span>
        </div>

        <h3>
          CONTENT PRIORITIES <Info size={14} />
        </h3>

        {Object.keys(left).map((key) => (
          <div className="slider" key={key}>
            <div>
              <span>{left[key]}</span>
              <span>{right[key]}</span>
            </div>

            <input
              type="range"
              min="0"
              max="100"
              value={prefs[key]}
              onChange={(e) => update(key, e.target.value)}
            />
          </div>
        ))}

        <button className="wide">
          <Settings size={16} /> Advanced preferences
        </button>
      </div>

      <div className="panel">
        <h3>
          CONTENT FILTERS <Info size={14} />
        </h3>

        {filters.map((filter) => (
          <label className="filter" key={filter}>
            {labels[filter]}

            <select
              value={prefs[filter]}
              onChange={(e) => {
                const next = {
                  ...prefs,
                  [filter]: e.target.value,
                };

                setPrefs(next);
                rank(next);
              }}
            >
              <option value="show_less">Show less</option>
              <option value="neutral">Neutral</option>
              <option value="show_more">Show more</option>
              <option value="limit">Limit</option>
            </select>
          </label>
        ))}
      </div>

      <div className="panel">
        <h3>
          FEED SOURCES <Info size={14} />
        </h3>

        <div className="donut"></div>

        {Object.entries(prefs.sources).map(([key, value]) => (
          <div className="source" key={key}>
            <span>{key.replace('_', ' ')}</span>
            <b>{value}%</b>
          </div>
        ))}

        <button className="wide">Edit source mix</button>
      </div>

      <div className="panel impact">
        <h3>
          FEED IMPACT <Info size={14} />
        </h3>

        <p>Since using Deep Focus mode</p>

        <div>
          ⏱️ <b>2h 15m</b> Time well spent
        </div>

        <div>
          🌱 <b>78%</b> Positive interactions
        </div>

        <div>
          🧠 <b>32%</b> More depth
        </div>

        <button className="wide">View your feed insights</button>
      </div>
    </aside>
  );
}

function MobileNav() {
  return (
    <div className="mobile">
      <Home />
      <Search />
      <Plus className="add" />
      <Bell />
      <User />
    </div>
  );
}

function timeAgo(date) {
  const hours = Math.max(
    1,
    Math.round((Date.now() - new Date(date)) / 3600000)
  );

  return hours < 24 ? `${hours}h` : `${Math.round(hours / 24)}d`;
}

createRoot(document.getElementById('root')).render(<App />);

import React, { useState } from 'react';
import './Insights.css';

const ARTICLES = [
  {
    id: 'shipping-faster',
    category: 'Engineering',
    author: 'Sara Patel',
    date: 'Mar 4, 2026',
    readTime: '6 min read',
    title: 'Shipping Faster Without Breaking Things',
    excerpt:
      'How small teams can balance <em>velocity</em> and reliability using feature flags, preview environments, and trunk-based development.',
    body: `
      <p>Speed and stability are often framed as opposites, but the best teams treat them as
      two sides of the same discipline. In this piece we break down the four habits that help
      our engineering pods ship daily without ever waking anyone up at 3am.</p>
      <h3>1. Trunk-based development</h3>
      <p>Long-lived branches are where bugs go to hide. We keep branches short (under 48 hours)
      and rely on <strong>feature flags</strong> to decouple deploy from release.</p>
      <h3>2. Preview environments</h3>
      <p>Every pull request gets a live URL. Designers, PMs and stakeholders can click through
      real flows before a single line hits production.</p>
      <h3>3. Fast, trustworthy tests</h3>
      <p>A test suite that takes 40 minutes is a test suite nobody runs locally. We aggressively
      parallelise and quarantine flakes within 24 hours.</p>
      <h3>4. Observability as a first class citizen</h3>
      <p>Logs, traces and metrics are wired up the same day a feature ships — not the week after
      the first incident.</p>
    `,
  },
  {
    id: 'design-systems',
    category: 'Design',
    author: 'Marcus Lee',
    date: 'Feb 18, 2026',
    readTime: '8 min read',
    title: 'Design Systems That Teams Actually Use',
    excerpt:
      'A design system is <em>not</em> a Figma library. It is a contract between product, design and engineering.',
    body: `
      <p>Most design systems die the same way: they start as a beautiful Figma file, get handed
      to engineering, and slowly rot as product pressure mounts. Here is how we keep ours alive.</p>
      <h3>Own the primitives first</h3>
      <p>Colour, spacing, typography and motion tokens should land before a single component.
      Without shared primitives, every component becomes an argument.</p>
      <h3>Write components once, skin them twice</h3>
      <p>Our button has one behaviour and four visual variants. That&#39;s it. Every time we let a
      fifth variant in, we regretted it within a quarter.</p>
      <h3>Measure adoption</h3>
      <p>If nobody uses your <code>&lt;Card&gt;</code> component, that&#39;s a signal — not a failure
      of the team. Sit with a product engineer for an afternoon and find the friction.</p>
    `,
  },
  {
    id: 'llm-cost',
    category: 'AI',
    author: 'Priya Nair',
    date: 'Jan 29, 2026',
    readTime: '5 min read',
    title: 'Keeping LLM Features Cheap in Production',
    excerpt:
      'Prompt caching, response streaming and model routing are the <em>three levers</em> that pulled our bill down 70%.',
    body: `
      <p>When we launched our AI contract review feature, our monthly inference bill briefly
      crossed five figures. Six weeks later it was back under $3k. Nothing clever — just
      three levers applied consistently.</p>
      <h3>Prompt caching</h3>
      <p>Long system prompts are expensive to re-send. Modern providers let you cache the
      static prefix and pay a fraction for subsequent calls. A one-line config change for us
      turned into a 40% cost drop.</p>
      <h3>Model routing</h3>
      <p>Not every task needs the frontier model. We route 80% of our calls to a smaller,
      cheaper model and only fall back to the flagship on ambiguous inputs.</p>
      <h3>Streaming + early exit</h3>
      <p>If the answer is already useful at token 200, don&#39;t wait for token 2000. Streaming
      plus a smart early-exit check shaves both latency and spend.</p>
    `,
  },
];

function Insights() {
  const [openId, setOpenId] = useState(null);

  const openArticle = ARTICLES.find(a => a.id === openId);

  if (openArticle) {
    return <ArticleView article={openArticle} onBack={() => setOpenId(null)} />;
  }

  return (
    <div className="insights">
      <section className="page-hero">
        <div className="page-hero-bg" />
        <div className="container">
          <div className="badge">Insights</div>
          <h1 className="section-title">
            Notes From the <span className="gradient-text">Nexus Team</span>
          </h1>
          <p className="section-desc">
            Lessons, experiments and opinions from the engineers, designers and strategists
            building with us every day.
          </p>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 48 }}>
        <div className="container">
          <div className="articles-grid">
            {ARTICLES.map(a => (
              <article className="card article-card" key={a.id}>
                <div className="article-meta">
                  <span className="article-category">{a.category}</span>
                  <span className="article-dot">•</span>
                  <span>{a.readTime}</span>
                </div>
                <h3 className="article-title">{a.title}</h3>
                <p
                  className="article-excerpt"
                  dangerouslySetInnerHTML={{ __html: a.excerpt }}
                />
                <div className="article-footer">
                  <div className="article-author">
                    <div className="author-avatar">
                      {a.author.split(' ').map(n => n[0]).join('')}
                    </div>
                    <div>
                      <div className="author-name">{a.author}</div>
                      <div className="author-date">{a.date}</div>
                    </div>
                  </div>
                  <button
                    className="btn btn-outline btn-sm"
                    onClick={() => setOpenId(a.id)}
                  >
                    Read →
                  </button>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

function ArticleView({ article, onBack }) {
  const [comments, setComments] = useState([
    {
      author: 'Jordan M.',
      date: 'Mar 5, 2026',
      text: 'Loved the point on preview environments — we rolled these out last quarter and PR review time dropped noticeably.',
    },
  ]);
  const [draft, setDraft] = useState({ author: '', text: '' });

  const submitComment = (e) => {
    e.preventDefault();
    if (!draft.author.trim() || !draft.text.trim()) return;
    const date = new Date().toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
    setComments(prev => [...prev, { author: draft.author, date, text: draft.text }]);
    setDraft({ author: '', text: '' });
  };

  return (
    <div className="insights">
      <section className="page-hero article-hero">
        <div className="page-hero-bg" />
        <div className="container">
          <button className="btn btn-outline btn-sm back-btn" onClick={onBack}>
            ← All insights
          </button>
          <div className="badge">{article.category}</div>
          <h1 className="section-title article-view-title">{article.title}</h1>
          <div className="article-meta article-meta-lg">
            <div className="author-avatar">
              {article.author.split(' ').map(n => n[0]).join('')}
            </div>
            <div>
              <div className="author-name">{article.author}</div>
              <div className="author-date">{article.date} · {article.readTime}</div>
            </div>
          </div>
        </div>
      </section>

      <section className="section" style={{ paddingTop: 40 }}>
        <div className="container article-body-wrap">
          <div
            className="article-body"
            dangerouslySetInnerHTML={{ __html: article.body }}
          />

          <div className="comments-section">
            <h2 className="comments-title">Discussion ({comments.length})</h2>
            <div className="divider" />

            <div className="comments-list">
              {comments.map((c, i) => (
                <div className="comment" key={i}>
                  <div className="comment-head">
                    <div className="author-avatar author-avatar-sm">
                      {c.author.trim().split(/\s+/).map(n => n[0]).join('').slice(0, 2)}
                    </div>
                    <div>
                      <div className="author-name">{c.author}</div>
                      <div className="author-date">{c.date}</div>
                    </div>
                  </div>
                  <div
                    className="comment-body"
                    dangerouslySetInnerHTML={{ __html: c.text }}
                  />
                </div>
              ))}
            </div>

            <form className="comment-form" onSubmit={submitComment}>
              <h3 className="comment-form-title">Join the conversation</h3>
              <div className="form-group">
                <label>Name</label>
                <input
                  type="text"
                  placeholder="Your name"
                  value={draft.author}
                  onChange={e => setDraft(d => ({ ...d, author: e.target.value }))}
                />
              </div>
              <div className="form-group">
                <label>Comment</label>
                <textarea
                  rows="4"
                  placeholder="Share your thoughts. Basic formatting supported."
                  value={draft.text}
                  onChange={e => setDraft(d => ({ ...d, text: e.target.value }))}
                />
              </div>
              <button type="submit" className="btn btn-primary">Post comment</button>
            </form>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Insights;

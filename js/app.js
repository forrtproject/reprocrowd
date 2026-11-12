(function () {
  'use strict';

  /* ---------- Tabs ---------- */
  var tabs = document.querySelectorAll('.main-nav .nav-tab');
  var panels = document.querySelectorAll('.tab-panel');
  var TAB_TITLE = 'ReproCrowd: crowdsourced numerical reproductions';
  var FRAGMENT = { landing: 'how-it-works', download: 'download', database: 'database', about: 'about' };
  var BY_FRAGMENT = {};
  Object.keys(FRAGMENT).forEach(function (k) { BY_FRAGMENT[FRAGMENT[k]] = k; });

  function activateTab(tab) {
    var name = tab.getAttribute('data-tab');
    tabs.forEach(function (t) {
      var active = t === tab;
      t.classList.toggle('is-active', active);
      t.setAttribute('aria-selected', active ? 'true' : 'false');
    });
    panels.forEach(function (p) {
      var show = p.id === 'panel-' + name;
      p.classList.toggle('is-active', show);
      p.hidden = !show;
    });
    var frag = FRAGMENT[name];
    if (frag && location.hash !== '#' + frag) {
      history.replaceState(null, '', '#' + frag);
    }
    document.title = tab.textContent.trim() + ' — ' + TAB_TITLE;
  }

  function tabForHash() {
    var h = location.hash.replace(/^#/, '');
    return BY_FRAGMENT[h] || null;
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () { activateTab(t); });
  });
  document.querySelectorAll('[data-goto-tab]').forEach(function (el) {
    el.addEventListener('click', function () {
      var name = el.getAttribute('data-goto-tab');
      var tab = document.querySelector('.main-nav .nav-tab[data-tab="' + name + '"]');
      if (tab) activateTab(tab);
    });
  });

  var brand = document.querySelector('.brand');
  if (brand) {
    brand.addEventListener('click', function (e) {
      e.preventDefault();
      var tab = document.querySelector('.main-nav .nav-tab[data-tab="landing"]');
      if (tab) activateTab(tab);
      window.scrollTo(0, 0);
    });
  }

  window.addEventListener('hashchange', function () {
    var name = tabForHash();
    if (name) {
      var tab = document.querySelector('.main-nav .nav-tab[data-tab="' + name + '"]');
      if (tab) activateTab(tab);
    }
  });

  var initial = tabForHash();
  var landingTab = document.querySelector('.main-nav .nav-tab[data-tab="landing"]');
  if (initial) {
    var it = document.querySelector('.main-nav .nav-tab[data-tab="' + initial + '"]');
    activateTab(it || landingTab);
  } else if (landingTab) {
    activateTab(landingTab);
  }

  /* ---------- Workflow chart (Mermaid) ---------- */
  if (window.mermaid) {
    mermaid.initialize({ startOnLoad: false, theme: 'neutral' });
    mermaid.run({ querySelector: '.tab-panel.is-active .mermaid' }).catch(function () {});
  }

  /* ---------- Copy prompt ---------- */
  var copyBtn = document.getElementById('copy-prompt');
  if (copyBtn) {
    function copyText(text) {
      var done = function () {
        copyBtn.textContent = 'Copied';
        setTimeout(function () { copyBtn.textContent = 'Copy'; }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done);
      } else {
        var ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    }
    copyBtn.addEventListener('click', function () {
      // The exact prompt is saved in prompt.txt; copy that, falling back to the inline text.
      fetch('./prompt.txt')
        .then(function (res) { return res.text(); })
        .then(function (text) { copyText(text.trim()); })
        .catch(function () {
          var code = document.querySelector('#prompt-text code');
          copyText(code ? code.textContent : '');
        });
    });
  }

  /* ---------- Upload, sign-off & submit ---------- */
  var input = document.getElementById('folder-input');
  var dropZone = document.getElementById('drop-zone');
  var status = document.getElementById('upload-status');
  var checklist = document.getElementById('checklist');
  var checklistList = document.getElementById('checklist-list');
  var actions = document.getElementById('upload-actions');
  var result = document.getElementById('submit-result');
  var submitBtn = document.getElementById('submit-btn');
  var downloadBtn = document.getElementById('download-btn');
  var selectedFiles = [];
  var topFolder = '';

  // Files needed for a ReproCrowd submission. Required = block submission; recommended = full reproducibility (optional).
  var REQUIRED = [
    { name: 'certificate.json', label: 'certificate.json', required: true },
    { name: 'certificate.md', label: 'certificate.md', required: true },
    { name: 'SIGN-OFF.md', label: 'SIGN-OFF.md', required: true },
    { name: 'flora-entry.json', label: 'flora-entry.json', required: true },
    { name: 'environment.json', label: 'environment.json (program inventory)', required: true },
    { name: 'myst.yml', label: '.yml config (myst.yml)', required: false },
    { name: 'pixi.toml', label: 'pixi.toml', required: false },
    { name: 'pixi.lock', label: 'pixi.lock', required: false },
    { name: 'Snakefile', label: 'Snakefile', required: false },
    { name: 'nanopubs/PUBLISHED.md', label: 'nanopubs/PUBLISHED.md', required: false },
    { name: 'CITATION.cff', label: 'CITATION.cff', required: false }
  ];

  var GITHUB_OWNER = 'LukasRoeseler';
  var GITHUB_REPO = 'reprocrowd';

  var signoff = document.getElementById('signoff');
  var signoffName = document.getElementById('signoff-name');
  var signoffOrcid = document.getElementById('signoff-orcid');
  var signoffRole = document.getElementById('signoff-role');
  var signoffAccept = document.getElementById('signoff-accept');

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function normalize(p) { return (p || '').replace(/\\/g, '/').toLowerCase(); }

  // Match a required path even when the whole folder is dropped (paths are prefixed with the folder name).
  function hasPath(found, name) {
    if (found.has(name)) return true;
    var suffix = '/' + name;
    return Array.from(found).some(function (p) { return p.endsWith(suffix); });
  }

  function handleFiles(fileList) {
    selectedFiles = [];
    topFolder = '';
    var paths = [];
    for (var i = 0; i < fileList.length; i++) {
      var f = fileList[i];
      var rel = (f.webkitRelativePath || f.name || '');
      paths.push(rel.replace(/\\/g, '/'));
      selectedFiles.push(f);
      if (!topFolder && rel) {
        var seg = rel.split(/[\\/]/)[0];
        if (seg) topFolder = seg;
      }
    }
    var found = new Set(paths.map(normalize));
    var requiredPresent = 0;
    var requiredTotal = 0;
    checklistList.innerHTML = '';
    REQUIRED.forEach(function (req) {
      var ok = hasPath(found, normalize(req.name));
      var li = document.createElement('li');
      var dot = document.createElement('span');
      dot.className = 'dot ' + (ok ? 'ok' : (req.required ? 'missing' : 'rec'));
      li.appendChild(dot);
      var text = req.label + (req.required ? '' : ' (recommended)');
      if (!ok && req.required) text += ' - missing';
      li.appendChild(document.createTextNode(text));
      checklistList.appendChild(li);
      if (req.required) { requiredTotal++; if (ok) requiredPresent++; }
    });
    checklist.hidden = false;
    var complete = requiredPresent === requiredTotal;
    signoff.hidden = !complete;
    actions.hidden = !complete;
    result.hidden = true;
    status.textContent = 'Selected ' + paths.length + ' file(s). ' + requiredPresent + '/' + requiredTotal + ' required files found.';
    if (complete) {
      status.textContent += ' Complete - sign off below to submit.';
    } else {
      status.textContent += ' Some required files are missing.';
    }
  }

  if (input) {
    input.addEventListener('change', function (e) { handleFiles(e.target.files); });
  }
  if (dropZone && input) {
    ['dragenter', 'dragover'].forEach(function (ev) {
      dropZone.addEventListener(ev, function (e) { e.preventDefault(); dropZone.classList.add('dragover'); });
    });
    ['dragleave', 'drop'].forEach(function (ev) {
      dropZone.addEventListener(ev, function (e) { e.preventDefault(); dropZone.classList.remove('dragover'); });
    });
    dropZone.addEventListener('drop', function (e) {
      if (e.dataTransfer && e.dataTransfer.files) handleFiles(e.dataTransfer.files);
    });
  }
  function slugFromTop() {
    var s = (topFolder || '').replace(/-certification$/i, '');
    return s || topFolder || '<slug>';
  }

  function downloadBundle() {
    if (!window.JSZip || !selectedFiles.length) {
      result.hidden = false;
      result.className = 'submit-result ok';
      result.innerHTML = '<strong>Almost there.</strong> Select the folder again, then click "Download bundle (.zip)".';
      return;
    }
    var zip = new JSZip();
    selectedFiles.forEach(function (f) {
      var rel = (f.webkitRelativePath || f.name || '');
      zip.file(rel, f);
    });
    zip.generateAsync({ type: 'blob' }).then(function (blob) {
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = (slugFromTop() || 'reprocrowd-certification') + '.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });
  }

  function issueUrl() {
    var slug = slugFromTop();
    var title = 'ReproCrowd certification: ' + slug;
    var body = 'Submit a ReproCrowd certification bundle.\n\n' +
      'Attach the zip of the `<slug>-certification` folder (use "Download bundle (.zip)").\n\n' +
      '- DOI:\n- Link to materials / data / code:\n- Engine / model / provider:\n- Repro standard version:\n- Outcome (computationally reproducible / computational issues / technical failure / computation not checked):';
    return 'https://github.com/' + GITHUB_OWNER + '/' + GITHUB_REPO +
      '/issues/new?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(body);
  }

  if (downloadBtn) {
    downloadBtn.addEventListener('click', downloadBundle);
  }

  if (submitBtn) {
    submitBtn.addEventListener('click', function () {
      var name = signoffName.value.trim();
      var orcid = signoffOrcid.value.trim();
      var role = signoffRole.value;
      var accepted = signoffAccept.checked;
      if (!name || !accepted) {
        result.hidden = false;
        result.className = 'submit-result ok';
        result.innerHTML = '<strong>Almost there.</strong> Enter your name and tick the acceptance box to sign off before submitting.';
        return;
      }
      result.hidden = false;
      result.className = 'submit-result ok';
      result.innerHTML =
        '<strong>Signed off by ' + escapeHtml(name) + ' (' + escapeHtml(role) +
        (orcid ? ' · ORCID ' + escapeHtml(orcid) : '') + ').</strong> ' +
        'The site is static and cannot write to GitHub for you. Pick a way to submit:' +
        '<p class="muted"><strong>No git? Easiest path.</strong> Download the bundle and attach it to a GitHub issue - ' +
        'the maintainer will merge it.</p>' +
        '<div class="btn-row">' +
        '<button class="btn" id="result-download">Download bundle (.zip)</button>' +
        '<a class="btn btn-primary" target="_blank" rel="noopener" href="' + issueUrl() + '">Open a GitHub issue (attach the zip)</a>' +
        '</div>' +
        '<p class="muted"><strong>With git.</strong> If you have write access, push straight to main; ' +
        'otherwise fork, push to a branch named <code>repro/&lt;slug&gt;</code>, and open a pull request:</p>' +
        '<pre class="git-cmds"><code>' +
        'git clone https://github.com/' + GITHUB_OWNER + '/' + GITHUB_REPO + '.git\n' +
        'cd ' + GITHUB_REPO + '\n' +
        'git checkout -b repro/&lt;slug&gt;\n' +
        '# copy your &lt;slug&gt;-certification folder in, e.g. into certifications/&lt;slug&gt;/\n' +
        'git add certifications/&lt;slug&gt;\n' +
        'git commit -m "Add ReproCrowd certification &lt;slug&gt;"\n' +
        'git push origin repro/&lt;slug&gt;</code></pre>' +
        '<p class="muted">Every submission lands under <code>certifications/&lt;slug&gt;/</code>. ' +
        'The commit (or the issue) is what saves the folder - there is nothing to upload via the site itself.</p>' +
        '<a class="btn" target="_blank" rel="noopener" href="https://github.com/' + GITHUB_OWNER + '/' + GITHUB_REPO + '">Open the repository</a>';
      var rd = document.getElementById('result-download');
      if (rd) rd.addEventListener('click', downloadBundle);
    });
  }

  /* ---------- Reproductions table (click a row to expand its chain) ---------- */
  var tbody = document.getElementById('repro-tbody');
  var search = document.getElementById('search');
  var filter = document.getElementById('filter-outcome');
  var empty = document.getElementById('empty');
  var count = document.getElementById('count');

  var rows = [];

  var ORCID_ICON = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSf8GIIkNF4uOKbDhPvV8aOzzaqj2Xx_4ePEYYSgCR_iwrsOEgbPsnLCfw&s=10';
  var COMMENT_URL = 'https://github.com/LukasRoeseler/reprocrowd/issues';

  /* SVG pictograms (no emojis) */
  var ICONS = {
    data: '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.2"><ellipse cx="8" cy="3.6" rx="5.6" ry="2.2"/><path d="M2.4 3.6v8.8c0 1.2 2.5 2.2 5.6 2.2s5.6-1 5.6-2.2V3.6"/><path d="M2.4 8c0 1.2 2.5 2.2 5.6 2.2S13.6 9.2 13.6 8"/></svg>',
    processed: '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="2" y="2" width="12" height="12" rx="1.4"/><path d="M2 6.2h12M2 10.4h12M6.2 2v12M10.4 2v12"/></svg>',
    code: '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 4 2 8l3 4M11 4l3 4-3 4M9.2 2.8 6.8 13.2"/></svg>',
    output: '<svg viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M2.5 14h11" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" fill="none"/><rect x="3.5" y="8.5" width="2.2" height="5.5" rx=".6"/><rect x="7" y="5" width="2.2" height="9" rx=".6"/><rect x="10.5" y="10" width="2.2" height="4" rx=".6"/></svg>',
    reported: '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"><path d="M4 1.6h5.5L12.5 4.6v9.8a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2.6a1 1 0 0 1 1-1z"/><path d="M9.5 1.6v3h3" stroke-linecap="round"/><path d="M5 8h6M5 10.4h6" stroke-linecap="round"/></svg>',
    claim: '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.2"><circle cx="8" cy="8" r="6"/><circle cx="8" cy="8" r="3.2"/><circle cx="8" cy="8" r="0.9" fill="currentColor" stroke="none"/></svg>',
    chev: '<svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3.5 11 8l-5 4.5"/></svg>',
    check: '<svg viewBox="0 0 16 16" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M3 8.5 6.5 12 13 4.5"/></svg>',
    cross: '<svg viewBox="0 0 16 16" width="10" height="10" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4l8 8M12 4l-8 8"/></svg>',
    comment: '<svg viewBox="0 0 16 16" width="14" height="14" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"><path d="M3 2.5h10a1 1 0 0 1 1 1v6a1 1 0 0 1-1 1H8l-3.4 2.8V10.5H3a1 1 0 0 1-1-1v-6a1 1 0 0 1 1-1z"/><path d="M5.5 6.2h5M5.5 8.4h3.4" stroke-linecap="round"/></svg>'
  };

  function pill(outcome) {
    var cls = 'pill-muted';
    if (outcome === 'computationally reproducible') cls = 'pill-ok';
    else if (outcome === 'computational issues') cls = 'pill-warn';
    else if (outcome === 'technical failure') cls = 'pill-bad';
    return '<span class="pill ' + cls + '">' + outcome + '</span>';
  }

  function fmtDate(d) {
    if (!d) return '-';
    var parts = d.split('-');
    return parts.length === 3 ? parts[2] + '/' + parts[1] + '/' + parts[0] : d;
  }

  function programsSummary(programs) {
    if (!programs || !programs.length) return '-';
    var text = programs.map(function (p) { return p.name + ' ' + p.version; }).join(' · ');
    var detail = programs.map(function (p) {
      var pkgs = p.packages ? Object.keys(p.packages).map(function (k) { return k + ' ' + p.packages[k]; }).join(', ') : '';
      return p.name + ' ' + p.version + (p.lockfile ? ' (' + p.lockfile + ')' : '') + (pkgs ? ' - ' + pkgs : '');
    }).join('\n');
    var safe = detail.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
    return '<span class="muted" title="' + safe + '">' + text + '</span>';
  }

  function ico(name) { return '<span class="ico">' + ICONS[name] + '</span>'; }

  function orcidLink(id) {
    if (!id) return '';
    return '<a class="orcid-link" href="https://orcid.org/' + escapeHtml(id) + '" target="_blank" rel="noopener" title="ORCID ' + escapeHtml(id) + '"><img class="orcid-icon" src="' + ORCID_ICON + '" alt="ORCID iD" /></a>';
  }

  function node(iconType, label, opts) {
    opts = opts || {};
    var cls = opts.cls ? ' ' + opts.cls : '';
    var t = opts.tooltip ? ' title="' + escapeHtml(opts.tooltip) + '"' : '';
    return '<div class="node' + cls + '"' + t + '>' + ico(iconType) + label + (opts.extra || '') + '</div>';
  }

  function rawGroup(r) {
    var srcs = r.raw_sources || [{ label: 'Raw data', available: true }];
    var multi = srcs.length > 1;
    var nodes = srcs.map(function (s) {
      var cls = 'data' + (s.available ? '' : ' na');
      var badge = s.available ? '' : '<span class="na-badge" title="Raw data not available — only processed data shipped">!</span>';
      var title = s.available ? 'Raw data available' : 'Raw data NOT available (grey link)';
      return node('data', escapeHtml(s.label), { cls: cls, tooltip: title, extra: badge });
    }).join('');
    var allNa = srcs.every(function (s) { return !s.available; });
    var link = '<span class="link h' + (allNa ? ' grey' : '') + '"></span>';
    return '<div class="raws' + (multi ? ' multi' : '') + '">' + nodes + '</div>' + link;
  }

  function spine(r) {
    return '<div class="spine">' + rawGroup(r) +
      node('processed', 'Processed data', { cls: 'wide' }) + '<span class="link h"></span>' +
      node('code', 'Code', { cls: 'wide' }) + '<span class="link h"></span>' +
      node('output', 'Output', { cls: 'output wide', tooltip: 'Single output produced by the code' }) +
      '</div>';
  }

  function claimBranch(c, reportUrl) {
    var ok = c.status === 'reproducible';
    var dot = '<span class="status ' + (ok ? 'ok' : 'bad') + '" title="' + escapeHtml(ok ? 'Reproduces' : 'Issue') + '">' + (ok ? ICONS.check : ICONS.cross) + '</span>';
    var tt = 'Reported: ' + c.reported + '\nReproduced: ' + c.reproduced + (c.note ? '\n' + c.note : '');
    var claimUrl = reportUrl + '#claim-' + c.id;
    return '<div class="claim ' + (ok ? 'good' : 'issue') + '">' +
      node('reported', 'Reported result', { tooltip: tt }) +
      '<span class="link h"></span>' +
      '<div class="node claim" title="' + escapeHtml(tt) + '">' + dot + ico('claim') +
      '<a href="' + escapeHtml(claimUrl) + '" target="_blank" rel="noopener">' + escapeHtml(c.label) + '</a></div>' +
      '</div>';
  }

  function detailCell(r) {
    var nOk = r.claims.filter(function (c) { return c.status === 'reproducible'; }).length;
    var nBad = r.claims.length - nOk;
    var srcs = r.raw_sources || [{ label: 'Raw data', available: true }];
    var mt = (srcs.length - 1) * 20;
    var claims = r.claims.map(function (c) { return claimBranch(c, r.report_url); }).join('');
    var head = '<div class="chain-head"><span>Provenance</span><span class="cnt">' + r.claims.length + ' claim' + (r.claims.length === 1 ? '' : 's') + '</span>' +
      '<span class="g">' + ICONS.check + ' ' + nOk + ' reproduces</span><span class="b">' + ICONS.cross + ' ' + nBad + ' issue</span>' +
      '<span>— ' + srcs.length + ' raw source' + (srcs.length === 1 ? '' : 's') + ' → one output → ' + r.claims.length + ' reported result' + (r.claims.length === 1 ? '' : 's') + '</span></div>';
    return '<div class="detail-wrap">' + head + '<div class="chain">' + spine(r) +
      '<div class="claims" style="margin-top:' + mt + 'px">' + claims + '</div></div></div>';
  }

  function rowCells(r) {
    var reportHref = r.report_url || r.repo_url;
    return '<td class="paper"><span class="chev">' + ICONS.chev + '</span><a class="title" href="' + escapeHtml(r.repo_url) + '" target="_blank" rel="noopener">' + escapeHtml(r.title || 'Untitled') + '</a><br><span class="doi">doi: ' + escapeHtml(r.doi || '') + '</span></td>' +
      '<td>' + escapeHtml(r.field || '-') + '</td>' +
      '<td>' + pill(r.outcome) + '</td>' +
      '<td>' + escapeHtml(r.engine || '-') + '<br><span class="muted">' + escapeHtml(r.model || '') + '</span></td>' +
      '<td>' + escapeHtml(r.repro_standard_version || '-') + '</td>' +
      '<td>' + programsSummary(r.programs) + '</td>' +
      '<td>' + (r.signature === 'signed' ? escapeHtml(r.signed_by || '') + ' ' + orcidLink(r.orcid) : '<span class="muted">—</span>') + '</td>' +
      '<td>' + fmtDate(r.date) + '</td>' +
      '<td class="report-cell">' +
        '<a class="report-link" href="' + escapeHtml(reportHref) + '" target="_blank" rel="noopener">Summary</a><br>' +
        '<a class="discuss-link" href="' + escapeHtml(COMMENT_URL) + '" target="_blank" rel="noopener">Discuss</a><br>' +
        '<a class="comment-badge" href="' + escapeHtml(COMMENT_URL) + '" target="_blank" rel="noopener" title="' + (r.comments || 0) + ' comment' + (r.comments === 1 ? '' : 's') + '">' + ICONS.comment +
          '<span class="badge-circle ' + (r.comments > 0 ? 'colored' : 'grey') + '">' + (r.comments || 0) + '</span></a>' +
      '</td>';
  }

  function render(list) {
    tbody.innerHTML = '';
    list.forEach(function (r) {
      var tr = document.createElement('tr');
      tr.className = 'article-row';
      tr.innerHTML = rowCells(r);
      var detail = document.createElement('tr');
      detail.className = 'detail-row';
      detail.innerHTML = '<td colspan="9">' + detailCell(r) + '</td>';
      detail.style.display = 'none';
      tr.addEventListener('click', function () {
        var open = detail.style.display !== 'none';
        detail.style.display = open ? 'none' : '';
        tr.classList.toggle('open', !open);
      });
      tbody.appendChild(tr);
      tbody.appendChild(detail);
    });
    empty.hidden = list.length > 0;
    count.textContent = list.length + ' reproduction(s) shown.';
  }

  function applyFilters() {
    var q = (search ? search.value : '').toLowerCase().trim();
    var oc = filter ? filter.value : '';
    var list = rows.filter(function (r) {
      if (oc && r.outcome !== oc) return false;
      if (!q) return true;
      var hay = [r.title, r.doi, r.field, r.outcome, r.model, r.engine, r.repro_standard_version].join(' ').toLowerCase();
      return hay.indexOf(q) !== -1;
    });
    render(list);
  }

  function load() {
    fetch('./data/reproductions.json')
      .then(function (res) { return res.json(); })
      .then(function (data) { rows = Array.isArray(data) ? data : []; applyFilters(); })
      .catch(function () { count.textContent = 'Could not load reproductions.'; });
  }

  if (search) search.addEventListener('input', applyFilters);
  if (filter) filter.addEventListener('change', applyFilters);

  load();
})();

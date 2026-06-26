class HaSidebarManagerRedirect extends HTMLElement {
  constructor() {
    super();
    this._target = null;
  }

  set panel(info) {
    this._target = info?.config?.target ?? null;
    this._redirect();
  }

  connectedCallback() {
    this._redirect();
  }

  _redirect() {
    const target = this._target;
    if (!target) {
      this.innerHTML = "<p style='padding:1em;font-family:sans-serif'>Keine Ziel-URL konfiguriert.</p>";
      return;
    }

    requestAnimationFrame(() => {
      if (window.history?.replaceState) {
        window.history.replaceState(null, "", target);
        window.dispatchEvent(
          new CustomEvent("location-changed", { detail: { replace: true } })
        );
      } else {
        window.location.href = target;
      }
    });
  }
}

if (!customElements.get("ha-sidebar-manager-redirect")) {
  customElements.define("ha-sidebar-manager-redirect", HaSidebarManagerRedirect);
}

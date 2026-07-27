document.addEventListener("DOMContentLoaded", () => {
    // Navigation Tabs
    const navSearch = document.getElementById("navSearch");
    const navCrm = document.getElementById("navCrm");
    const viewSearch = document.getElementById("viewSearch");
    const viewCrm = document.getElementById("viewCrm");

    // Search Elements
    const searchForm = document.getElementById("searchForm");
    const cityInput = document.getElementById("cityInput");
    const categorySelect = document.getElementById("categorySelect");
    const btnSubmitSearch = document.getElementById("btnSubmitSearch");

    const metricsRow = document.getElementById("metricsRow");
    const metricTotal = document.getElementById("metricTotal");
    const metricNoWeb = document.getElementById("metricNoWeb");
    const metricOutdated = document.getElementById("metricOutdated");
    const metricCritical = document.getElementById("metricCritical");

    const searchLoader = document.getElementById("searchLoader");
    const loaderStatusText = document.getElementById("loaderStatusText");
    const resultsSection = document.getElementById("resultsSection");
    const resultsTableBody = document.getElementById("resultsTableBody");
    const tableSearch = document.getElementById("tableSearch");
    const btnExportCsv = document.getElementById("btnExportCsv");

    const filterPills = document.querySelectorAll(".pill");
    const countAll = document.getElementById("countAll");
    const countNoWeb = document.getElementById("countNoWeb");
    const countOutdated = document.getElementById("countOutdated");
    const countModern = document.getElementById("countModern");

    // CRM Elements
    const crmTableBody = document.getElementById("crmTableBody");
    const crmSearch = document.getElementById("crmSearch");

    // Pitch Modal Elements
    const pitchModal = document.getElementById("pitchModal");
    const btnCloseModal = document.getElementById("btnCloseModal");
    const modalBizName = document.getElementById("modalBizName");
    const textWa = document.getElementById("textWa");
    const btnWaDirect = document.getElementById("btnWaDirect");
    const textEmailSubject = document.getElementById("textEmailSubject");
    const textEmailBody = document.getElementById("textEmailBody");
    const btnEmailDirect = document.getElementById("btnEmailDirect");
    const textPhone = document.getElementById("textPhone");

    // Notes Modal Elements
    const notesModal = document.getElementById("notesModal");
    const btnCloseNotesModal = document.getElementById("btnCloseNotesModal");
    const notesBizName = document.getElementById("notesBizName");
    const notesLeadId = document.getElementById("notesLeadId");
    const notesInput = document.getElementById("notesInput");
    const btnSaveNotes = document.getElementById("btnSaveNotes");

    // State
    let currentResults = [];
    let savedCrmLeads = [];
    let activeFilter = "all";
    let lastSearchedCity = "";
    let activePitchBiz = null;

    // NAVIGATION TABS SWITCH
    navSearch.addEventListener("click", () => {
        navSearch.classList.add("active");
        navCrm.classList.remove("active");
        viewSearch.classList.remove("hidden");
        viewCrm.classList.add("hidden");
    });

    navCrm.addEventListener("click", async () => {
        navCrm.classList.add("active");
        navSearch.classList.remove("active");
        viewCrm.classList.remove("hidden");
        viewSearch.classList.add("hidden");
        await loadCrmLeads();
    });

    // 1. SEARCH FORM SUBMIT
    searchForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const city = cityInput.value.trim();
        const category = categorySelect.value;
        if (!city) return;

        lastSearchedCity = city;

        btnSubmitSearch.disabled = true;
        searchLoader.classList.remove("hidden");
        resultsSection.classList.add("hidden");
        metricsRow.classList.add("hidden");
        loaderStatusText.innerText = `Ricerca e audit in corso per "${city}"...`;

        try {
            const resp = await fetch("/api/search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ city, category })
            });

            const data = await resp.json();

            if (!resp.ok) {
                alert(data.error || "Errore durante la ricerca.");
                return;
            }

            currentResults = data.results || [];

            metricTotal.innerText = data.metrics.total;
            metricNoWeb.innerText = data.metrics.no_website;
            metricOutdated.innerText = data.metrics.outdated_or_insecure;
            metricCritical.innerText = data.metrics.critical_opportunity;

            countAll.innerText = data.metrics.total;
            countNoWeb.innerText = data.metrics.no_website;
            countOutdated.innerText = data.metrics.outdated_or_insecure;
            countModern.innerText = data.metrics.total - (data.metrics.no_website + data.metrics.outdated_or_insecure);

            metricsRow.classList.remove("hidden");
            resultsSection.classList.remove("hidden");
            btnExportCsv.disabled = currentResults.length === 0;

            renderTable();

        } catch (err) {
            console.error(err);
            alert("Errore di connessione al server.");
        } finally {
            btnSubmitSearch.disabled = false;
            searchLoader.classList.add("hidden");
        }
    });

    // 2. RENDER RESULTS TABLE
    function renderTable() {
        resultsTableBody.innerHTML = "";
        const query = tableSearch.value.toLowerCase().trim();

        const filtered = currentResults.filter(item => {
            if (activeFilter === "no_website" && item.has_website) return false;
            if (activeFilter === "outdated" && (!item.has_website || (!item.is_outdated_design && !item.is_http_only && item.is_responsive))) return false;
            if (activeFilter === "modern" && (!item.has_website || item.is_outdated_design || item.is_http_only || !item.is_responsive)) return false;

            if (query) {
                const nameMatch = item.name.toLowerCase().includes(query);
                const addressMatch = item.address.toLowerCase().includes(query);
                return nameMatch || addressMatch;
            }

            return true;
        });

        if (filtered.length === 0) {
            resultsTableBody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:2rem; color:var(--text-muted);">Nessuna attività trovata.</td></tr>`;
            return;
        }

        filtered.forEach(item => {
            const tr = document.createElement("tr");

            // Social Icons
            let socialHtml = "";
            if (item.instagram_url) {
                socialHtml += `<a href="${item.instagram_url}" target="_blank" class="social-icon instagram" title="Instagram"><i class="fa-brands fa-instagram"></i></a>`;
            }
            if (item.facebook_url) {
                socialHtml += `<a href="${item.facebook_url}" target="_blank" class="social-icon facebook" title="Facebook"><i class="fa-brands fa-facebook-f"></i></a>`;
            }

            // Website Badge
            let webHtml = `<span class="badge-status badge-critical">🔴 Nessun Sito</span>`;
            if (item.has_website) {
                const isWarning = item.is_http_only || item.is_outdated_design || !item.is_responsive;
                const badgeColor = isWarning ? "badge-high" : "badge-low";
                webHtml = `
                    <a href="${item.url}" target="_blank" class="contact-info">
                        <span class="badge-status ${badgeColor}">${isWarning ? '🟡 Sito Obsoleto/Non Sicuro' : '🟢 Sito Attivo'}</span>
                        <small style="margin-top:2px; font-size:0.75rem;">${escapeHtml(item.url)}</small>
                    </a>
                `;
            }

            // CRM Select Box
            const crmStatus = item.crm_status || "new";
            const crmNotes = item.crm_notes || "";

            tr.innerHTML = `
                <td>
                    <div class="biz-name">${escapeHtml(item.name)}</div>
                    <div class="biz-category"><i class="fa-solid fa-tag"></i> ${escapeHtml(item.category)}</div>
                </td>
                <td>
                    <div class="contact-info">
                        ${item.phone ? `<div><i class="fa-solid fa-phone"></i> <a href="tel:${item.phone}">${escapeHtml(item.phone)}</a></div>` : ''}
                        ${item.email ? `<div><i class="fa-solid fa-envelope"></i> <a href="mailto:${item.email}">${escapeHtml(item.email)}</a></div>` : ''}
                        <div><i class="fa-solid fa-map-pin"></i> <a href="${item.google_maps_url}" target="_blank">Google Maps</a></div>
                        ${socialHtml ? `<div class="social-links">${socialHtml}</div>` : ''}
                    </div>
                </td>
                <td>${webHtml}</td>
                <td>
                    <span class="score-tag ${item.opportunity_score >= 80 ? 'text-danger' : ''}">${item.opportunity_score}/100</span>
                </td>
                <td>
                    <select class="crm-select status-${crmStatus}" data-id="${item.lead_id}">
                        <option value="new" ${crmStatus === 'new' ? 'selected' : ''}>🔴 Da Contattare</option>
                        <option value="contacted" ${crmStatus === 'contacted' ? 'selected' : ''}>🟡 Messaggio Inviato</option>
                        <option value="meeting" ${crmStatus === 'meeting' ? 'selected' : ''}>🔵 In Trattativa</option>
                        <option value="won" ${crmStatus === 'won' ? 'selected' : ''}>🟢 Cliente Acquisito!</option>
                        <option value="lost" ${crmStatus === 'lost' ? 'selected' : ''}>❌ Non Interessato</option>
                    </select>
                    <button class="btn-icon btn-note" data-id="${item.lead_id}" data-name="${escapeHtml(item.name)}" data-note="${escapeHtml(crmNotes)}" title="Aggiungi/Modifica Nota">
                        <i class="fa-solid fa-note-sticky" style="${crmNotes ? 'color:var(--accent-cyan);' : ''}"></i>
                    </button>
                </td>
                <td class="text-right">
                    <button class="btn btn-secondary btn-sm btn-pitch" data-name="${escapeHtml(item.name)}">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Pitch
                    </button>
                </td>
            `;

            // Attach Event Listeners
            const crmSelect = tr.querySelector(".crm-select");
            crmSelect.addEventListener("change", (e) => updateCrmStatus(item, e.target.value, crmSelect));

            const btnNote = tr.querySelector(".btn-note");
            btnNote.addEventListener("click", () => openNotesModal(item));

            const btnPitch = tr.querySelector(".btn-pitch");
            btnPitch.addEventListener("click", () => openPitchModal(item));

            resultsTableBody.appendChild(tr);
        });
    }

    // 3. CRM STATUS UPDATE
    async function updateCrmStatus(bizItem, newStatus, selectEl) {
        selectEl.className = `crm-select status-${newStatus}`;
        bizItem.crm_status = newStatus;

        try {
            await fetch("/api/crm/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    lead_id: bizItem.lead_id,
                    status: newStatus,
                    biz_data: bizItem
                })
            });
        } catch (err) {
            console.error("Error updating CRM status:", err);
        }
    }

    // 4. NOTES MODAL
    function openNotesModal(bizItem) {
        notesBizName.innerText = bizItem.name;
        notesLeadId.value = bizItem.lead_id;
        notesInput.value = bizItem.crm_notes || "";
        notesModal.classList.remove("hidden");
    }

    btnSaveNotes.addEventListener("click", async () => {
        const leadId = notesLeadId.value;
        const noteText = notesInput.value.trim();

        const bizItem = currentResults.find(b => b.lead_id === leadId) || savedCrmLeads.find(b => b.lead_id === leadId)?.biz_data;
        if (bizItem) {
            bizItem.crm_notes = noteText;
        }

        try {
            await fetch("/api/crm/update", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    lead_id: leadId,
                    notes: noteText
                })
            });
            notesModal.classList.add("hidden");
            renderTable();
            if (!viewCrm.classList.contains("hidden")) loadCrmLeads();
        } catch (err) {
            alert("Errore durante il salvataggio della nota.");
        }
    });

    btnCloseNotesModal.addEventListener("click", () => notesModal.classList.add("hidden"));

    // 5. LOAD CRM SAVED LEADS
    async function loadCrmLeads() {
        try {
            const resp = await fetch("/api/crm");
            savedCrmLeads = await resp.json();
            renderCrmTable();
        } catch (err) {
            console.error("Error loading CRM:", err);
        }
    }

    function renderCrmTable() {
        crmTableBody.innerHTML = "";
        const query = crmSearch.value.toLowerCase().trim();

        const filtered = savedCrmLeads.filter(lead => {
            const biz = lead.biz_data || {};
            const name = (biz.name || "").toLowerCase();
            const city = (biz.city || "").toLowerCase();
            return !query || name.includes(query) || city.includes(query);
        });

        if (filtered.length === 0) {
            crmTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; padding:2rem; color:var(--text-muted);">Nessun lead salvato nel CRM.</td></tr>`;
            return;
        }

        filtered.forEach(lead => {
            const biz = lead.biz_data || {};
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>
                    <div class="biz-name">${escapeHtml(biz.name || lead.lead_id)}</div>
                    <div class="biz-category">${escapeHtml(biz.city || '')} - ${escapeHtml(biz.category || '')}</div>
                </td>
                <td>
                    <div class="contact-info">
                        ${biz.phone ? `<div><i class="fa-solid fa-phone"></i> ${escapeHtml(biz.phone)}</div>` : ''}
                        ${biz.email ? `<div><i class="fa-solid fa-envelope"></i> ${escapeHtml(biz.email)}</div>` : ''}
                    </div>
                </td>
                <td>
                    <select class="crm-select status-${lead.status}">
                        <option value="new" ${lead.status === 'new' ? 'selected' : ''}>🔴 Da Contattare</option>
                        <option value="contacted" ${lead.status === 'contacted' ? 'selected' : ''}>🟡 Messaggio Inviato</option>
                        <option value="meeting" ${lead.status === 'meeting' ? 'selected' : ''}>🔵 In Trattativa</option>
                        <option value="won" ${lead.status === 'won' ? 'selected' : ''}>🟢 Cliente Acquisito!</option>
                        <option value="lost" ${lead.status === 'lost' ? 'selected' : ''}>❌ Non Interessato</option>
                    </select>
                </td>
                <td>
                    <span style="font-size:0.85rem; color:var(--text-muted);">${escapeHtml(lead.notes || 'Nessuna nota')}</span>
                </td>
                <td class="text-right">
                    <button class="btn btn-secondary btn-sm btn-pitch-crm">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> Pitch
                    </button>
                </td>
            `;

            const selectEl = tr.querySelector(".crm-select");
            selectEl.addEventListener("change", (e) => updateCrmStatus(biz, e.target.value, selectEl));

            const btnPitch = tr.querySelector(".btn-pitch-crm");
            btnPitch.addEventListener("click", () => openPitchModal(biz));

            crmTableBody.appendChild(tr);
        });
    }

    crmSearch.addEventListener("input", renderCrmTable);

    // 6. OPEN PITCH MODAL & DIRECT 1-CLICK LINKS
    async function openPitchModal(item) {
        activePitchBiz = item;
        modalBizName.innerText = item.name;
        pitchModal.classList.remove("hidden");

        textWa.value = "Generazione messaggio...";
        textEmailSubject.value = "";
        textEmailBody.value = "Generazione corpo email...";
        textPhone.value = "Generazione script...";

        try {
            const resp = await fetch("/api/pitch", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    name: item.name,
                    city: item.city || lastSearchedCity,
                    phone: item.phone,
                    email: item.email,
                    website: item.url,
                    audit: item
                })
            });

            const pitch = await resp.json();
            textWa.value = pitch.whatsapp;
            textEmailSubject.value = pitch.email_subject;
            textEmailBody.value = pitch.email_body;
            textPhone.value = pitch.phone_script;

            // Setup WhatsApp 1-Click Link
            const rawPhone = (item.phone || "").replace(/[^0-9]/g, "");
            const waPhone = rawPhone.startsWith("39") ? rawPhone : (rawPhone ? "39" + rawPhone : "");
            const encodedWaMsg = encodeURIComponent(pitch.whatsapp);
            if (waPhone) {
                btnWaDirect.href = `https://web.whatsapp.com/send?phone=${waPhone}&text=${encodedWaMsg}`;
            } else {
                btnWaDirect.href = `https://web.whatsapp.com/send?text=${encodedWaMsg}`;
            }

            // Setup Email 1-Click Link
            const encodedSub = encodeURIComponent(pitch.email_subject);
            const encodedBody = encodeURIComponent(pitch.email_body);
            btnEmailDirect.href = `mailto:${item.email || ''}?subject=${encodedSub}&body=${encodedBody}`;

        } catch (err) {
            console.error(err);
        }
    }

    // Modal Events
    btnCloseModal.addEventListener("click", () => pitchModal.classList.add("hidden"));
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
            btn.classList.add("active");
            document.getElementById(btn.dataset.tab).classList.add("active");
        });
    });

    document.querySelectorAll(".btn-copy").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetEl = document.getElementById(btn.dataset.target);
            if (targetEl) {
                targetEl.select();
                navigator.clipboard.writeText(targetEl.value);
                const orig = btn.innerHTML;
                btn.innerHTML = `<i class="fa-solid fa-check"></i> Copiato!`;
                setTimeout(() => { btn.innerHTML = orig; }, 2000);
            }
        });
    });

    // Filter pills & search filter
    filterPills.forEach(pill => {
        pill.addEventListener("click", () => {
            filterPills.forEach(p => p.classList.remove("active"));
            pill.classList.add("active");
            activeFilter = pill.dataset.filter;
            renderTable();
        });
    });
    tableSearch.addEventListener("input", renderTable);

    // Export CSV
    btnExportCsv.addEventListener("click", () => {
        if (currentResults.length === 0) return;

        const headers = ["Nome Attivita", "Categoria", "Citta", "Telefono", "Email", "Sito Web", "Ha Sito", "Sito Obsoleto", "Score Lead", "Stato CRM", "Note", "Instagram", "Facebook"];
        const csvRows = [headers.join(",")];

        currentResults.forEach(item => {
            const row = [
                `"${item.name.replace(/"/g, '""')}"`,
                `"${(item.category || '').replace(/"/g, '""')}"`,
                `"${(item.city || lastSearchedCity).replace(/"/g, '""')}"`,
                `"${(item.phone || '').replace(/"/g, '""')}"`,
                `"${(item.email || '').replace(/"/g, '""')}"`,
                `"${(item.url || '').replace(/"/g, '""')}"`,
                item.has_website ? "SI" : "NO",
                item.is_outdated_design ? "SI" : "NO",
                item.opportunity_score,
                `"${item.crm_status || 'new'}"`,
                `"${(item.crm_notes || '').replace(/"/g, '""')}"`,
                `"${(item.instagram_url || '').replace(/"/g, '""')}"`,
                `"${(item.facebook_url || '').replace(/"/g, '""')}"`
            ];
            csvRows.push(row.join(","));
        });

        const csvContent = "data:text/csv;charset=utf-8,\uFEFF" + csvRows.join("\n");
        const link = document.createElement("a");
        link.setAttribute("href", encodeURI(csvContent));
        link.setAttribute("download", `leadscout_${lastSearchedCity}_${new Date().toISOString().slice(0,10)}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

    function escapeHtml(text) {
        if (!text) return "";
        return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
    }
});

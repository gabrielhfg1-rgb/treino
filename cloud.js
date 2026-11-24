// Conexão com o Firebase: login com Google e banco de dados (Firestore).
// Cada pessoa só lê e grava dentro de users/<seu id>/..., e as regras do
// arquivo firestore.rules garantem isso no servidor.
import { firebaseConfig } from './firebase-config.js';

const V = '10.14.1';
const configured = !!(firebaseConfig && firebaseConfig.apiKey && !/COLE/i.test(firebaseConfig.apiKey));

async function start() {
  if (!configured) return { configured: false };

  const { initializeApp } = await import(`https://www.gstatic.com/firebasejs/${V}/firebase-app.js`);
  const A = await import(`https://www.gstatic.com/firebasejs/${V}/firebase-auth.js`);
  const F = await import(`https://www.gstatic.com/firebasejs/${V}/firebase-firestore.js`);

  const app = initializeApp(firebaseConfig);
  const auth = A.getAuth(app);
  await A.setPersistence(auth, A.browserLocalPersistence).catch(() => {});
  let fs;
  try {
    // guarda uma cópia no aparelho: o app abre e salva mesmo sem internet
    fs = F.initializeFirestore(app, { localCache: F.persistentLocalCache({ tabManager: F.persistentMultipleTabManager() }) });
  } catch (e) {
    fs = F.getFirestore(app);
  }

  const firstUser = new Promise(resolve => {
    const off = A.onAuthStateChanged(auth, u => { off(); resolve(u); });
  });

  let uid = null;
  const p = path => `users/${uid}/${path}`;
  const wrapDoc = s => ({ id: s.id, exists: s.exists(), data: () => s.data(), metadata: s.metadata });
  const docApi = path => {
    const ref = () => F.doc(fs, p(path));
    return {
      id: path.split('/').pop(), path,
      get: async () => wrapDoc(await F.getDoc(ref())),
      set: data => F.setDoc(ref(), data),
      update: data => F.updateDoc(ref(), data),
      delete: () => F.deleteDoc(ref()),
      onSnapshot: (next, err) => F.onSnapshot(ref(), { includeMetadataChanges: false }, s => next(wrapDoc(s)), e => err && err(e)),
    };
  };
  const collApi = path => ({
    path,
    doc: id => docApi(`${path}/${id || F.doc(F.collection(fs, p(path))).id}`),
    onSnapshot: (next, err) => F.onSnapshot(F.collection(fs, p(path)), s => next({
      docs: s.docs.map(wrapDoc), size: s.size, empty: s.empty, metadata: s.metadata,
    }), e => err && err(e)),
  });

  return {
    configured: true,
    db: { doc: docApi, collection: collApi },
    async user() {
      const u = auth.currentUser || await firstUser;
      uid = u ? u.uid : null;
      return u;
    },
    async signIn() {
      const provider = new A.GoogleAuthProvider();
      provider.setCustomParameters({ prompt: 'select_account' });
      try {
        await A.signInWithPopup(auth, provider);
      } catch (e) {
        if (e && e.code === 'auth/popup-blocked') return A.signInWithRedirect(auth, provider);
        throw e;
      }
    },
    signOut: () => A.signOut(auth),
  };
}

start()
  .then(api => window.__cloudResolve(api))
  .catch(err => {
    console.error('Firebase não carregou:', err);
    window.__cloudResolve({ configured: false, error: String(err) });
  });

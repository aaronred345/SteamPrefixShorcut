# Maintainer: Aaron Gerbert <aaronred345@gmail.com>
pkgname=steam-prefix-shortcut
pkgver=1.1.0
pkgrel=1
pkgdesc="Creates symbolic links to Proton/Wine prefixes for Steam games running through Proton"
arch=('any')
url="https://github.com/aaronred345/SteamPrefixShorcut"
license=('MIT')
depends=('python')
source=("$pkgname-$pkgver.tar.gz::$url/archive/refs/tags/v$pkgver.tar.gz")
sha256sums=('5f65ff9696ab00bfbf0f8d162430d496df680a385fd1f013457112ebd9817f93')

package() {
    cd "$srcdir/SteamPrefixShorcut-$pkgver"
    install -Dm755 main.py "$pkgdir/usr/bin/steam-prefix"
    install -Dm644 LICENSE "$pkgdir/usr/share/licenses/$pkgname/LICENSE"
    install -dm755 "$pkgdir/etc/profile.d"
    printf '%s\n' '/usr/bin/steam-prefix > /dev/null 2>&1 &' \
        > "$pkgdir/etc/profile.d/steam-prefix.sh"
    chmod 644 "$pkgdir/etc/profile.d/steam-prefix.sh"
}

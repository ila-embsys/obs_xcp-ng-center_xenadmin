pkgname=xenadmin
pkgver=0
pkgrel=0
pkgdesc="XCP-ng Center is a management tool for XCP-ng environments"
arch=('x86_64')
url="https://github.com/ila-embsys/xenadmin.git"
license=('BSD-2-Clause')
groups=('base-devel')
makedepends=(
    'mono-msbuild'
    'git'
    'ttf-roboto'
)
source=(
    ${pkgname}-${pkgver}.tar.gz
    nuget_packages.tgz
    mono-app-exec.template
)
  sha256sums=(
    "SKIP"
    "08ccbec53016efdb9a0ca71fc31ea3d75a2add97dfb39b72bf9da827c4174e13"
    "c673c8a36fcb1b65e52d846e0c3e3e3817f973e037a5f62591bede2df66f7629"
  )

prepare() {
  cd "${srcdir}"/${pkgname}-${pkgver}
  mkdir -p nuget_packages
  tar -xf ${srcdir}/nuget_packages.tgz -C nuget_packages
  msbuild -t:restore -p:RestorePackagesPath=nuget_packages
}

build() {
  cd "${srcdir}"/${pkgname}-${pkgver}
  msbuild -p:Configuration=Release

  mkdir -p usr/bin

  LIBDIR="/usr/lib" \
  APPLICATION="$pkgname" \
  EXECUTABLE="XCP-ng Center" \
  envsubst < ${srcdir}/mono-app-exec.template > usr/bin/$pkgname
}

package() {
  cd "${srcdir}"/${pkgname}-${pkgver}

  install -Dm 755 usr/bin/$pkgname $pkgdir/usr/bin/$pkgname

	cd XenAdmin/bin/Release/net48
	find . -type f ! -path '*.pdb' -exec \
		install -Dm 644 "{}" "$pkgdir/usr/lib/xenadmin/{}" \;
}

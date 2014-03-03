#include "stdafx.h"

using namespace System;
using namespace System::Reflection;
using namespace System::Runtime::CompilerServices;
using namespace System::Runtime::InteropServices;
using namespace System::Security::Permissions;

//
// La información general sobre un ensamblado se controla mediante el siguiente
// conjunto de atributos. Cambie estos atributos para modificar la información
// asociada con un ensamblado.
//
[assembly:AssemblyTitleAttribute("opencvtest")];
[assembly:AssemblyDescriptionAttribute("")];
[assembly:AssemblyConfigurationAttribute("")];
[assembly:AssemblyCompanyAttribute("")];
[assembly:AssemblyProductAttribute("opencvtest")];
[assembly:AssemblyCopyrightAttribute("Copyright (c)  2013")];
[assembly:AssemblyTrademarkAttribute("")];
[assembly:AssemblyCultureAttribute("")];

//
// La información de versión de un ensamblado consta de los cuatro valores siguientes:
//
//      Versión principal
//      Versión secundaria
//      Número de compilación
//      Revisión
//
// Puede especificar todos los valores o usar los valores predeterminados de número de compilación y de revisión
// mediante el asterisco ('*'), como se muestra a continuación:

[assembly:AssemblyVersionAttribute("1.0.*")];

[assembly:ComVisible(false)];

[assembly:CLSCompliantAttribute(true)];

[assembly:SecurityPermission(SecurityAction::RequestMinimum, UnmanagedCode = true)];

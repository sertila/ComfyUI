# ComfyUI Update and Restart - Quick Start

This repository now includes automated update scripts for ComfyUI!

## 🚀 Quick Usage

### Linux/Mac
```bash
./update_and_restart.sh
```

### Windows
```batch
update_and_restart.bat
```

### Python (All Platforms)
```bash
python update_comfyui.py
```

## 📋 What Gets Updated

1. **ComfyUI Core** - Latest changes from the repository
2. **Custom Nodes** - All installed custom nodes (if they are git repositories)
3. **Python Dependencies** - All packages in requirements.txt

## 📖 Full Documentation

For detailed information, troubleshooting, and advanced usage, see [UPDATE_GUIDE.md](UPDATE_GUIDE.md)

## ⚠️ Important Notes

- **Backup First**: Always backup your workflows and custom settings before updating
- **Check Compatibility**: Review release notes for breaking changes
- **Test First**: Consider testing updates in a development environment

## 🔄 Restart After Update

The wrapper scripts (`update_and_restart.sh` and `update_and_restart.bat`) will automatically:
- Detect if ComfyUI is running
- Offer to restart it after updates
- Handle the shutdown and startup process

For manual restart:
1. Stop ComfyUI (Ctrl+C or close the window)
2. Start it again: `python main.py`

## 🆘 Getting Help

If you encounter issues:
- Check [UPDATE_GUIDE.md](UPDATE_GUIDE.md) for troubleshooting
- Review ComfyUI GitHub issues: https://github.com/comfyanonymous/ComfyUI/issues
- Join the ComfyUI Discord: https://discord.gg/comfyui

## 📝 Update Frequency

Recommended schedule:
- **Weekly**: ComfyUI core updates
- **As needed**: Custom nodes
- **Monthly**: Python dependencies

---

**Made with ❤️ for the ComfyUI community**
